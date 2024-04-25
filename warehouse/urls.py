from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/manager/', views.dashboard_manager, name='manager_dashboard'),
    path('mahsulotlar/', views.mahsulot_list, name='mahsulotlar'),
    path('mahsulot_crud/', views.mahsulot_crud, name='mahsulot_crud'),
    path('get_product_data/', views.get_product_data, name='get_product_data'),
    path('send_product/', views.send_product, name='send_product'),
    path('product_history/', views.product_history, name='product_history'),
    path('dashboard_charts_data/', views.dashboard_charts_data,
         name='dashboard_charts_data'),


    # login
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # customers
    path('customers/', views.customers, name='customers'),
    path('customer_crud/', views.customer_crud, name='customer_crud'),
]
