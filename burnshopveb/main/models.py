from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField('Название категории', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

class Product(models.Model):
    name = models.CharField('Название товара', max_length=200)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    discount_price = models.DecimalField('Цена со скидкой', max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    brand = models.CharField('Бренд', max_length=100)
    image = models.ImageField('Изображение товара', upload_to='products/', blank=True)
    stock = models.PositiveIntegerField('Количество на складе')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

class Promotion(models.Model):
    name = models.CharField('Название акции', max_length=200)
    discount_percentage = models.DecimalField('Процент скидки', max_digits=5, decimal_places=2)
    start_date = models.DateTimeField('Дата начала')
    end_date = models.DateTimeField('Дата окончания')

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    is_active.boolean = True
    is_active.short_description = 'Активна'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    rating = models.PositiveIntegerField('Оценка')
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f'Review for {self.product.name} by {self.user.username}'

    def short_comment(self, obj):
        if obj.comment:
            return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
        return ''

    short_comment.short_description = 'Комментарий'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    added_at = models.DateTimeField('Дата добавления',auto_now_add=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['-added_at']
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'
