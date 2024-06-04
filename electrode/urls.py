from django.urls import path
from . import views


urlpatterns = [
    path('', views.electrode, name='elektrod'),
    path('electrode_crud/', views.electrode_crud, name='electrode_crud'),
    path('api/labels/', views.labels_api, name='labels_api'),
    path('api/categories/', views.categories_api, name='categories_api'),
    path('get_electrode_data/', views.get_electrode_data,
         name='get_electrode_data'),
]
