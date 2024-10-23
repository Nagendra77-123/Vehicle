from django.urls import path
from . import views

urlpatterns = [
    path('register_component/', views.register_component, name='register_component'),
    path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('add_issue/<int:vehicle_id>/', views.add_issue, name='add_issue'),
    path('vehicles/<int:vehicle_id>/calculate_price/', views.calculate_price, name='calculate_price'),
]
