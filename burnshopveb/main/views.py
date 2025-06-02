from django.shortcuts import render
from django.db.models import Avg, Count
from django.utils import timezone
from .models import Product, Category, Promotion, Review

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
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    return render(
        request,
        'main/search_results.html',
        {'products': products, 'query': query}
    )