from django.urls import path
from .views import home, search_results, product_detail, product_list, product_edit, product_delete, product_add, register, user_login, user_logout, category_products, toggle_wishlist, wishlist

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_results, name='search_results'),
    path('products/', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('product/edit/<int:pk>/', product_edit, name='product_edit'),
    path('product/delete/<int:pk>/', product_delete, name='product_delete'),
    path('product/add/', product_add, name='product_add'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('category/<int:pk>/', category_products, name='category_products'),
    path('wishlist/toggle/<int:pk>/', toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', wishlist, name='wishlist'),
]