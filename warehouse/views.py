from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Mahsulot, ProductHistory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
            # if user.is_manager:
            #     return redirect('manager_dashboard')
            # else:
            #     return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'auth/login.html')


@login_required
def dashboard(request):
    total_products = Mahsulot.objects.count()
    total_customers = Customer.objects.count()

    recently_edited = ProductHistory.objects.order_by(
        '-timestamp').values('product_id', 'transaction_type')[:5]
    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'recently_edited': recently_edited,

    }
    return render(request, 'warehouse/dashboard.html', context)


def dashboard_charts_data(request):
    most_products = Mahsulot.objects.order_by(
        '-miqdori')[:5].values('nomi', 'miqdori')
    most_received = ProductHistory.objects.filter(transaction_type='Addition').values(
        'product_id').annotate(total_received=Count('product_id')).order_by('-total_received')[:5]
    most_sent = ProductHistory.objects.filter(transaction_type='Substraction').values(
        'product_id').annotate(total_sent=Count('product_id')).order_by('-total_sent')[:5]
    data = {
        'most_products': list(most_products),
        # 'recently_edited': list(recently_edited),
        'most_received': list(most_received),
        'most_sent': list(most_sent)
    }

    return JsonResponse(data)


def dashboard_manager(request):
    mahsulotlar = Mahsulot.objects.all()
    return render(request, 'warehouse/manager_dashboard.html', {'mahsulotlar': mahsulotlar})


@login_required
def mahsulot_list(request):
    mahsulotlar = Mahsulot.objects.all()
    customers = Customer.objects.all()
    user = request.user
    is_manager = request.user.is_manager

    return render(request, 'warehouse/mahsulotlar.html',
                  {'mahsulotlar': mahsulotlar, 'customers': customers,
                   'profile_pic': user.photo.url if user.photo else 'default-profile-pic-url', 'is_manager': is_manager})


@csrf_exempt
@login_required
def mahsulot_crud(request):
    # Check user role
    if request.user.is_manager and request.method != 'GET':
        return JsonResponse({'error': 'You do not have permission to perform this action.'}, status=403)

    if request.method == 'GET':
        mahsulotlar = list(Mahsulot.objects.values())
        return JsonResponse(mahsulotlar, safe=False)

    elif request.method == 'POST':
        if request.user.is_manager:
            return JsonResponse({'error': 'You do not have permission to perform this action.'}, status=403)
        nomi = request.POST.get('nomi')
        kategoriya = request.POST.get('kategoriya')
        qadoq = request.POST.get('qadoq')
        quti = request.POST.get('quti')
        massa = request.POST.get('massa')
        miqdori = request.POST.get('miqdori')
        kelgan_sana = request.POST.get('kelgan_sana')
        tavsifi = request.POST.get('tavsifi')

        existing_product = Mahsulot.objects.filter(
            nomi=nomi, kategoriya=kategoriya).first()

        if existing_product:
            existing_product.miqdori += int(miqdori)
            existing_product.qadoq += int(qadoq)
            existing_product.quti += int(quti)
            existing_product.save()
            # Log history of adding product
            item = ProductHistory.objects.create(
                product_id=existing_product.pk,
                transaction_type='Addition',
                quantity=miqdori
            )
            item.save()
            return JsonResponse({'message': 'Mahsulot quantity updated successfully', 'mahsulot_id': existing_product.pk})
        else:
            mahsulot = Mahsulot.objects.create(
                nomi=nomi,
                kategoriya=kategoriya,
                qadoq=qadoq,
                quti=quti,
                massa=massa,
                miqdori=miqdori,
                kelgan_sana=kelgan_sana,
                tavsifi=tavsifi
            )
            # Log history of adding product
            ProductHistory.objects.create(
                product_id=mahsulot.pk,
                transaction_type='ADD',
                quantity=miqdori
            )
            return JsonResponse({'message': 'Mahsulot created successfully', 'mahsulot_id': mahsulot.pk})

    elif request.method == 'PUT':
        if request.user.is_manager:
            return JsonResponse({'error': 'You do not have permission to perform this action.'}, status=403)

        data = json.loads(request.body)
        mahsulot_id = data.get('id')
        if not mahsulot_id:
            return JsonResponse({'error': 'ID is required for updating'}, status=400)

        try:
            mahsulot = Mahsulot.objects.get(pk=mahsulot_id)
        except Mahsulot.DoesNotExist:
            return JsonResponse({'error': 'Mahsulot does not exist'}, status=404)
        existing_amount = mahsulot.miqdori

        yangi_qadoq = data.get('qadoq', mahsulot.qadoq)
        yangi_quti = data.get('quti', mahsulot.quti)
        yangi_massa = data.get('massa', mahsulot.massa)
        yangi_miqdori = data.get('miqdori', mahsulot.miqdori)

        mahsulot.nomi = data.get('nomi', mahsulot.nomi)
        mahsulot.kategoriya = data.get('kategoriya', mahsulot.kategoriya)
        # mahsulot.qadoq = data.get('qadoq', mahsulot.qadoq)
        # mahsulot.quti = data.get('quti', mahsulot.quti)
        # mahsulot.massa = data.get('massa', mahsulot.massa)
        # mahsulot.miqdori = data.get('miqdori', mahsulot.miqdori)
        mahsulot.qadoq += int(yangi_qadoq)
        mahsulot.quti += int(yangi_quti)
        mahsulot.massa += int(yangi_massa)
        mahsulot.miqdori += int(yangi_miqdori)
        mahsulot.kelgan_sana = data.get('kelgan_sana', mahsulot.kelgan_sana)
        mahsulot.tavsifi = data.get('tavsifi', mahsulot.tavsifi)
        mahsulot.save()

        added_amount = int(mahsulot.miqdori) - int(existing_amount)
        product = get_object_or_404(Mahsulot, id=mahsulot_id)
        ProductHistory.objects.create(
            product=product,
            transaction_type='ADD',
            quantity=yangi_miqdori
        )
        return JsonResponse({'message': 'Mahsulot updated successfully'})

    elif request.method == 'DELETE':
        if request.user.is_manager:
            return JsonResponse({'error': 'You do not have permission to perform this action.'}, status=403)
        data = json.loads(request.body)
        mahsulot_id = data.get('id')
        if not mahsulot_id:
            return JsonResponse({'error': 'ID is required for deletion'}, status=400)

        try:
            mahsulot = Mahsulot.objects.get(pk=mahsulot_id)
        except Mahsulot.DoesNotExist:
            return JsonResponse({'error': 'Mahsulot does not exist'}, status=404)

        mahsulot.delete()
        return JsonResponse({'message': 'Mahsulot deleted successfully'})


# @login_required
@csrf_exempt
def send_product(request):
    if request.method == 'POST':
        if request.user.is_manager:
            return JsonResponse({'error': 'You do not have permission to perform this action.'}, status=403)
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        customer_id = data.get('customer_id')

        if not (product_id and quantity and customer_id):
            return JsonResponse({'error': 'Product ID, quantity, and customer ID are required'}, status=400)

        try:
            product = Mahsulot.objects.get(pk=product_id)
            customer = Customer.objects.get(pk=customer_id)
        except (Mahsulot.DoesNotExist, Customer.DoesNotExist):
            return JsonResponse({'error': 'Product or customer does not exist'}, status=404)

        if product.miqdori < int(quantity):
            return JsonResponse({'error': 'Not enough quantity available'}, status=400)

        product.miqdori -= int(quantity)
        product.save()
        # ProductHistory.objects.create(
        #     product_id=product_id,
        #     customer_id=customer_id,
        #     transaction_type='Substraction',
        #     quantity=quantity
        # )
        ProductHistory.objects.create(
            product=product,
            customer=customer,
            transaction_type='SEND',  # Using the choice from ACTION_CHOICES
            quantity=int(quantity)
        )

        return JsonResponse({'message': 'Product sent successfully'})


@csrf_exempt
def get_product_data(request):
    if request.method == 'GET':
        product_id = request.GET.get('id')
        try:
            product = Mahsulot.objects.get(pk=product_id)
            product_data = {
                'id': product.id,
                'nomi': product.nomi,
                'kategoriya': product.kategoriya,
                'qadoq': product.qadoq,
                'quti': product.quti,
                'massa': product.massa,
                'miqdori': product.miqdori,
                'kelgan_sana': product.kelgan_sana,
                'tavsifi': product.tavsifi
            }
            return JsonResponse(product_data)
        except Mahsulot.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist'}, status=404)


@login_required
def customers(request):
    customers = Customer.objects.all()
    is_manager = request.user.is_manager
    return render(request, 'warehouse/customers.html', {'customers': customers, 'is_manager': is_manager})


# Forbidden(CSRF token missing.) error in this view --- error fixed.
# @login_required
@csrf_exempt
def customer_crud(request, id=None):
    if request.user.is_manager and request.method != 'GET':
        return JsonResponse({'error': 'You do not have permission to perform this action.'}, status=403)

    if request.method == 'GET':
        if request.GET.get('id'):
            customer_id = request.GET.get('id')
            customer = get_object_or_404(Customer, id=customer_id)
            return JsonResponse({'customer': {
                'id': customer.pk,
                'name': customer.name,
                'location': customer.location,
                'phone_number': customer.phone_number,
            }})
        else:
            customers = list(Customer.objects.values())
            return JsonResponse(customers, safe=False)

    elif request.method == 'POST':
        if request.user.is_manager:
            return JsonResponse({'error': 'You do not have permission to perform this action.'}, status=403)
        name = request.POST.get('customerName')
        location = request.POST.get('customerLocation')
        phone_number = request.POST.get('customerPhoneNumber')
        customer = Customer.objects.create(
            name=name, location=location, phone_number=phone_number)
        return JsonResponse({'message': 'Customer created successfully', 'customer_id': customer.pk})

    elif request.method == 'PUT':
        if request.user.is_manager:
            return JsonResponse({'error': 'You do not have permission to perform this action.'}, status=403)

        data = json.loads(request.body)
        customer_id = data.get('id')
        customer = get_object_or_404(Customer, id=customer_id)
        customer.name = data.get('name', customer.name)
        customer.location = data.get('location', customer.location)
        customer.phone_number = data.get('phone_number', customer.phone_number)
        customer.save()
        return JsonResponse({'message': 'Customer updated successfully'})

    elif request.method == 'DELETE':
        if request.user.is_manager:
            return JsonResponse({'error': 'You do not have permission to perform this action.'}, status=403)
        try:
            data = json.loads(request.body)
            customer_id = data.get('id')
            print("this is id:", customer_id)

            if not customer_id:
                print("id not found", customer_id)
                return JsonResponse({'error': 'ID is required for deletion'}, status=400)
            customer = Customer.objects.get(id=customer_id)
            customer.delete()
            return JsonResponse({'message': 'Customer deleted successfully'})

        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer does not exist'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


# history
@login_required
def product_history(request):
    history = ProductHistory.objects.all().order_by('-timestamp')
    return render(request, 'warehouse/product_history.html', {'history': history})


def get_product_name(product_id):
    product = get_object_or_404(Mahsulot, id=product_id)
    return product.nomi
