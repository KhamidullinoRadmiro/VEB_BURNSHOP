from django.urls import path
from .views import home, search_results, product_detail, product_list, product_edit, product_delete, product_add

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_results, name='search_results'),
    path('products/', product_list, name='product_list'),  # Список товаров
    path('product/<int:pk>/', product_detail, name='product_detail'),  # Детали товара
    path('product/edit/<int:pk>/', product_edit, name='product_edit'),  # Редактирование
    path('product/delete/<int:pk>/', product_delete, name='product_delete'),  # Удаление
    path('product/add/', product_add, name='product_add'),  # Добавление
]