from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg, Count
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Product, Review, Promotion, Category, Wishlist
from .forms import ProductForm, UserRegisterForm, UserLoginForm

def home(request):
    top_products = Product.objects.annotate(
        avg_rating=Avg('review__rating')
    ).order_by('-avg_rating')[:5]

    active_promotions = Promotion.objects.filter(
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    )

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
    if query:
        products = Product.objects.filter(
            name__icontains=query
        ) | Product.objects.filter(
            brand__icontains=query
        ) | Product.objects.filter(
            description__icontains=query
        )
    else:
        products = Product.objects.none()
    return render(request, 'main/search_results.html', {'products': products, 'query': query})

def product_list(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        for product in products:
            product.is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    return render(request, 'main/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    is_in_wishlist = request.user.is_authenticated and Wishlist.objects.filter(user=request.user, product=product).exists()
    return render(request, 'main/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'is_in_wishlist': is_in_wishlist
    })

@user_passes_test(lambda u: u.is_superuser, login_url='home')
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

@user_passes_test(lambda u: u.is_superuser, login_url='home')
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

def category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)
    if request.user.is_authenticated:
        for product in products:
            product.is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    return render(request, 'main/category_products.html', {'category': category, 'products': products})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Регистрация успешна! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли!')
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'main/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли!')
    return redirect('home')

@login_required
def toggle_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        wishlist_item.delete()
        messages.success(request, f'Товар "{product.name}" удалён из избранного.')
    else:
        messages.success(request, f'Товар "{product.name}" добавлен в избранное.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'main/wishlist.html', {'wishlist_items': wishlist_items})