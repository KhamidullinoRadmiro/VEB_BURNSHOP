from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg, Count
from django.utils import timezone
from .models import Product, Review, Promotion, Category
from .forms import ProductForm

def home(request):
    # Популярные товары (Top-5 по среднему рейтингу)
    top_products = Product.objects.annotate(
        avg_rating=Avg('review__rating')
    ).order_by('-avg_rating')[:5]

    # Текущие акции
    active_promotions = Promotion.objects.filter(
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    )

    # Категории с количеством товаров
    categories_with_count = Category.objects.annotate(
        product_count=Count('product')
    )

    return render(
        request,
        'main/home.html',
        {
            'top_products': top_products,
            'active_promotions': active_promotions,
            'categories_with_count': categories_with_count,
        }
    )

def search_results(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query) | Product.objects.filter(brand__icontains=query)
    return render(request, 'main/search_results.html', {'products': products, 'query': query})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'main/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    return render(request, 'main/product_detail.html', {'product': product, 'reviews': reviews, 'avg_rating': avg_rating})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно обновлён!')
            return redirect('product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'main/product_edit.html', {'form': form, 'product': product})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Товар успешно удалён!')
        return redirect('product_list')
    return render(request, 'main/product_delete.html', {'product': product})

def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно добавлен!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'main/product_add.html', {'form': form})