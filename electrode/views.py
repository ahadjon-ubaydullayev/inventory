from django.shortcuts import render
from django.http import JsonResponse
from .models import Electrode, ElectrodeCategory, ElectrodeLabel
import json
from django.views.decorators.csrf import csrf_exempt


def electrode(request):
    electrodes = Electrode.objects.all()
    for electrode in electrodes:
        electrode.count_by_label = Electrode.objects.filter(
            label=electrode.label).count()
    return render(request, 'electrode.html', {'electrodes': electrodes})


@csrf_exempt
def electrode_crud(request):
    if request.method == 'GET':
        electrodes = Electrode.objects.all().values()
        return JsonResponse(list(electrodes), safe=False)

    if request.method == 'POST':
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
        try:
            data = json.loads(request.body)
            print(data)
            electrode_id = data.get('id')
            label = data.get('label')
            category = data.get('category')
            package = data.get('package')
            electrode = Electrode.objects.get(pk=electrode_id)
            electrode.label = label
            electrode.category = category
            electrode.package = package
            print(data)
            electrode.save()
            return JsonResponse({'message': 'Electrode updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    # Handle other HTTP methods if needed
    return JsonResponse({'error': 'Method not allowed'}, status=405)


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
