from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Mahsulot
import json
from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


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
            if user.is_manager:
                return redirect('manager_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'auth/login.html')


def dashboard(request):
    mahsulotlar = Mahsulot.objects.all()
    print(request.user.is_authenticated)
    return render(request, 'warehouse/dashboard.html', {'mahsulotlar': mahsulotlar, 'user': request.user})


def dashboard_manager(request):
    mahsulotlar = Mahsulot.objects.all()
    return render(request, 'warehouse/manager_dashboard.html', {'mahsulotlar': mahsulotlar})


def mahsulot_list(request):
    mahsulotlar = Mahsulot.objects.all()
    return render(request, 'warehouse/mahsulotlar.html', {'mahsulotlar': mahsulotlar})


@csrf_exempt
def mahsulot_crud(request):
    if request.method == 'GET':
        mahsulotlar = list(Mahsulot.objects.values())
        return JsonResponse(mahsulotlar, safe=False)

    elif request.method == 'POST':
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
            # If the product exists, update its quantity
            existing_product.miqdori += int(miqdori)
            existing_product.qadoq += int(qadoq)
            existing_product.quti += int(quti)
            existing_product.save()
            return JsonResponse({'message': 'Mahsulot quantity updated successfully', 'mahsulot_id': existing_product.pk})
        else:
            # If the product doesn't exist, create a new one
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
            return JsonResponse({'message': 'Mahsulot created successfully', 'mahsulot_id': mahsulot.pk})

    elif request.method == 'PUT':
        data = json.loads(request.body)
        mahsulot_id = data.get('id')
        if not mahsulot_id:
            return JsonResponse({'error': 'ID is required for updating'}, status=400)

        try:
            mahsulot = Mahsulot.objects.get(pk=mahsulot_id)
        except Mahsulot.DoesNotExist:
            return JsonResponse({'error': 'Mahsulot does not exist'}, status=404)

        mahsulot.nomi = data.get('nomi', mahsulot.nomi)
        mahsulot.kategoriya = data.get('kategoriya', mahsulot.kategoriya)
        mahsulot.qadoq = data.get('qadoq', mahsulot.qadoq)
        mahsulot.quti = data.get('quti', mahsulot.quti)
        mahsulot.massa = data.get('massa', mahsulot.massa)
        mahsulot.miqdori = data.get('miqdori', mahsulot.miqdori)
        mahsulot.kelgan_sana = data.get('kelgan_sana', mahsulot.kelgan_sana)
        mahsulot.tavsifi = data.get('tavsifi', mahsulot.tavsifi)

        mahsulot.save()
        return JsonResponse({'message': 'Mahsulot updated successfully'})

    elif request.method == 'DELETE':
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
