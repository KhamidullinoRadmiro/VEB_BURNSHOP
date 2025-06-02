from django.shortcuts import render
from .models import Product, Category

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'main/home.html', {'products': products, 'categories': categories})