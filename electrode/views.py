from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Electrode, ElectrodeCategory, ElectrodeLabel, ElectrodeHistory
import json
from django.views.decorators.csrf import csrf_exempt
from warehouse.models import Customer
from django.contrib.auth import authenticate, login, logout


def electrode(request):
    customers = Customer.objects.all()
    electrodes = Electrode.objects.all()
    is_manager = request.user.is_manager
    for electrode in electrodes:
        electrode.count_by_label = Electrode.objects.filter(
            label=electrode.label).count()
    return render(request, 'electrode.html', {'electrodes': electrodes, 'customers': customers, 'is_manager': is_manager})


@csrf_exempt
def electrode_crud(request):
    # Check user role
    if request.user.is_manager and request.method != 'GET':
        return JsonResponse({'error': 'You do not have permission to perform this action.'}, status=403)

    if request.method == 'GET':
        electrodes = Electrode.objects.all().values()
        return JsonResponse(list(electrodes), safe=False)

    if request.method == 'POST':
        if request.user.is_manager:
            return JsonResponse({'error': 'You do not have permission to perform this action.'}, status=403)
        try:
            data = json.loads(request.body)
            label_id = data.get('label_id')
            category_id = data.get('category_id')
            package = data.get('package')
            # box = data.get('box')
            # weight = data.get('weight')
            # count_by_label = data.get('count_by_label')
            description = data.get('description')

            category = ElectrodeCategory.objects.get(id=category_id)
            if category.category_name == '4':
                box = int(package) / 4
                weight = int(package) * 5

            elif category.category_name == '3' or category.category_name == '2.5':
                box = int(package) / 8
                weight = int(package) * 2.5

            else:
                box = package / 2
                weight = package * 2.5

            existing_electrode = Electrode.objects.filter(
                label=label_id, category=category_id).first()

            if existing_electrode:
                print("electrode exists", existing_electrode.label,
                      existing_electrode, existing_electrode.category)
                # Update the existing electrode's attributes
                existing_electrode.package += int(package)
                print(existing_electrode.package)
                existing_electrode.box += int(box)
                existing_electrode.weight = weight
                existing_electrode.description = description  # Update the description if needed
                existing_electrode.save()  # Save the updated electrode
                return JsonResponse({'message': 'Mahsulot quantity updated successfully', 'mahsulot_id': existing_electrode.pk})

            else:

                electrode = Electrode.objects.create(
                    label_id=label_id,
                    category_id=category_id,
                    package=package,
                    box=box,
                    weight=weight,
                    # count_by_label=count_by_label,
                    description=description
                )

                return JsonResponse({'message': 'Electrode created successfully', 'electrode_id': electrode.pk})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'PUT':
        if request.user.is_manager:
            return JsonResponse({'error': 'You do not have permission to perform this action.'}, status=403)
        try:
            data = json.loads(request.body)
            electrode_id = data.get('id')
            existing_electrode_count = Electrode.objects.get(
                id=electrode_id).package
            # label = data.get('label')
            # category = data.get('category')
            label_name = data.get('label')  # You are receiving the label name
            category_name = data.get('category')
            label = ElectrodeLabel.objects.get(label_name=label_name)
            category = ElectrodeCategory.objects.get(
                label=label, category_name=category_name)

            package = data.get('package')

            electrode = Electrode.objects.get(pk=electrode_id)

            electrode.label = label
            electrode.category = category
            electrode.package = existing_electrode_count + int(package)
            electrode.save()

            # Log history entry
            ElectrodeHistory.objects.create(
                electrode=electrode,
                transaction_type='ADD',  # Assuming this is an addition
                quantity=package,  # Assuming package is the quantity for addition
                description='Electrode updated'
            )
            return JsonResponse({'message': 'Electrode updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        if request.user.is_manager:
            return JsonResponse({'error': 'You do not have permission to perform this action.'}, status=403)
        try:
            data = json.loads(request.body)
            electrode_id = data.get('id')
            if not electrode_id:
                return JsonResponse({'error': 'ID is required for deletion'}, status=400)

            electrode = Electrode.objects.get(pk=electrode_id)
            electrode.delete()
            return JsonResponse({'message': 'Electrode deleted successfully'})
        except Electrode.DoesNotExist:
            return JsonResponse({'error': 'Electrode does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_electrode_data(request):
    if request.method == 'GET' and 'id' in request.GET:
        electrode_id = request.GET.get('id')
        try:
            electrode = Electrode.objects.get(pk=electrode_id)
            data = {
                'id': electrode.id,
                'label': electrode.label.label_name,
                'category': electrode.category.category_name,
                'package': electrode.package,
                # Add other fields as needed
            }
            return JsonResponse(data)
        except Electrode.DoesNotExist:
            return JsonResponse({'error': 'Electrode not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method or missing ID parameter'}, status=400)


@csrf_exempt
def send_electrode(request):
    if request.method == 'POST':
        if request.user.is_manager:
            return JsonResponse({'error': 'You do not have permission to perform this action.'}, status=403)
        try:
            data = json.loads(request.body)
            electrode_id = data.get('electrode_id')
            quantity = data.get('quantity')
            customer_id = data.get('customer_id')
            if not (electrode_id and quantity and customer_id):
                return JsonResponse({'error': 'Electrode ID, quantity, and customer ID are required'}, status=400)

            quantity = int(quantity)

            electrode = get_object_or_404(Electrode, pk=electrode_id)
            customer = get_object_or_404(Customer, pk=customer_id)

            if electrode.package < quantity:
                return JsonResponse({'error': 'Not enough quantity available in the package'}, status=400)

            # Reduce the package quantity
            electrode.package -= quantity
            electrode.save()

            # Log history entry
            ElectrodeHistory.objects.create(
                electrode=electrode,
                transaction_type='SEND',
                quantity=quantity,
                customer=customer,
                description=f'Electrode sent to {customer.name}'
            )
            print("cus id", customer_id)

            # Optionally, you might want to log this action, notify the customer, etc.

            return JsonResponse({'message': 'Electrode sent successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def labels_api(request):
    if request.method == 'GET':
        labels = ElectrodeLabel.objects.all().values()
        return JsonResponse(list(labels), safe=False)
    elif request.method == 'POST':
        # Handle POST request to create a new label (if needed)
        pass  # Add your logic here


def categories_api(request):
    if request.method == 'GET':
        label_id = request.GET.get('label_id')
        if label_id is not None:
            categories = ElectrodeCategory.objects.filter(
                label_id=label_id).values()
        else:
            categories = ElectrodeCategory.objects.all().values()
        return JsonResponse(list(categories), safe=False)
    elif request.method == 'POST':
        # Handle POST request to create a new category (if needed)
        pass  # Add your logic here


def electrode_history(request):
    history = ElectrodeHistory.objects.all().order_by('-timestamp')
    return render(request, 'electrode_history.html', {'history': history})
