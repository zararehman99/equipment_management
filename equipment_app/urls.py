from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('inventory/', views.inventory_view, name='inventory_view'),
    path('add_to_reservation/<int:equipment_id>/', views.add_to_reservation, name='add_to_reservation'),
    path('remove_reservation/<int:reservation_id>/', views.remove_reservation, name='remove_reservation'),
    path('login/register/', views.register_view, name='register'),
    path('view_reservations/', views.view_reservations, name='view_reservations'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
]



