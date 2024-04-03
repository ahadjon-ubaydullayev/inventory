from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/manager/', views.dashboard_manager, name='manager_dashboard'),
    path('mahsulotlar/', views.mahsulot_list, name='mahsulotlar'),
    path('mahsulot_crud/', views.mahsulot_crud, name='mahsulot_crud'),

    # login
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
