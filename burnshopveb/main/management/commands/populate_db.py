from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Category, Product, Order, OrderItem, Review, Wishlist, Promotion
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with initial data'

    def handle(self, *args, **kwargs):
        # Создаём пользователей
        for i in range(1, 11):
            User.objects.get_or_create(username=f'user{i}', defaults={'password': 'password123'})

        # Создаём категории
        categories = ['Наушники', 'Клавиатуры', 'Мыши', 'Мониторы', 'Аксессуары']
        for name in categories:
            Category.objects.get_or_create(name=name)

        # Создаём товары
        brands = ['Logitech', 'Razer', 'HyperX', 'SteelSeries', 'Corsair']
        for i in range(1, 21):  # 20 товаров
            category = random.choice(Category.objects.all())
            Product.objects.get_or_create(
                name=f'Product {i}',
                description=f'Description for Product {i}',
                price=random.uniform(20, 200),
                discount_price=random.uniform(15, 180) if random.choice([True, False]) else None,
                category=category,
                brand=random.choice(brands),
                image=f'products/product{i}.jpg',  # Предполагается, что ты добавишь изображения
                stock=random.randint(1, 100)
            )

        # Создаём акции
        for i in range(1, 11):
            start_date = timezone.now() - timedelta(days=random.randint(1, 10))
            end_date = start_date + timedelta(days=random.randint(5, 15))
            Promotion.objects.get_or_create(
                name=f'Promotion {i}',
                discount_percentage=random.uniform(5, 50),
                start_date=start_date,
                end_date=end_date
            )

        # Создаём заказы
        for i in range(1, 11):
            user = User.objects.get(username=f'user{i}')
            order = Order.objects.get_or_create(
                user=user,
                total_amount=0,
                status='в обработке',
                delivery_address=f'Address {i}'
            )[0]
            total = 0
            for j in range(random.randint(1, 5)):
                product = random.choice(Product.objects.all())
                quantity = random.randint(1, 3)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
                total += product.price * quantity
            order.total_amount = total
            order.save()

        # Создаём отзывы
        for i in range(1, 21):
            Review.objects.get_or_create(
                user=random.choice(User.objects.all()),
                product=random.choice(Product.objects.all()),
                rating=random.randint(1, 5),
                comment=f'Review {i}'
            )

        # Создаём избранное
        for i in range(1, 15):
            Wishlist.objects.get_or_create(
                user=random.choice(User.objects.all()),
                product=random.choice(Product.objects.all())
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))