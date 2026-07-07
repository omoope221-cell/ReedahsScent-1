from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('admin-login/', views.dashboard_login, name='login'),
    path('admin-logout/', views.dashboard_logout, name='logout'),
    path('admin-dashboard/', views.dashboard_home, name='home'),

    path('admin-dashboard/products/', views.product_list, name='product_list'),
    path('admin-dashboard/products/add/', views.product_create, name='product_create'),
    path('admin-dashboard/products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('admin-dashboard/products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    path('admin-dashboard/categories/', views.category_list, name='category_list'),
    path('admin-dashboard/categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('admin-dashboard/orders/', views.order_list, name='order_list'),
    path('admin-dashboard/orders/<int:pk>/', views.order_detail, name='order_detail'),
]
