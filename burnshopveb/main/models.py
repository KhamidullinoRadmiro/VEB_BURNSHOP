from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Название категории")
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Родительская категория")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Дата обновления")
    )

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name=_("Название товара")
    )
    description = models.TextField(
        verbose_name=_("Описание")
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Цена")
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Цена со скидкой")
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_("Категория")
    )
    brand = models.CharField(
        max_length=100,
        verbose_name=_("Бренд")
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name=_("Изображение")
    )
    stock = models.IntegerField(
        verbose_name=_("Количество на складе")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Дата обновления")
    )

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    def __str__(self):
        return f"{self.name} ({self.brand})"


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь")
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Общая сумма")
    )
    status = models.CharField(
        max_length=50,
        default='в обработке',
        verbose_name=_("Статус")
    )
    delivery_address = models.TextField(
        verbose_name=_("Адрес доставки")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Дата обновления")
    )

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")

    def __str__(self):
        return f"Заказ {self.id} от {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_("Заказ")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Товар")
    )
    quantity = models.IntegerField(
        verbose_name=_("Количество")
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Цена")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания")
    )

    class Meta:
        verbose_name = _("Элемент заказа")
        verbose_name_plural = _("Элементы заказов")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Товар")
    )
    rating = models.IntegerField(
        verbose_name=_("Рейтинг")
    )
    comment = models.TextField(
        verbose_name=_("Комментарий")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Дата обновления")
    )

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")

    def __str__(self):
        return f"Отзыв на {self.product.name} от {self.user.username}"


class Wishlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Товар")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата добавления")
    )

    class Meta:
        verbose_name = _("Избранное")
        verbose_name_plural = _("Избранное")

    def __str__(self):
        return f"{self.product.name} в избранном {self.user.username}"


class Promotion(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Название акции")
    )
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Процент скидки")
    )
    start_date = models.DateTimeField(
        verbose_name=_("Дата начала")
    )
    end_date = models.DateTimeField(
        verbose_name=_("Дата окончания")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания")
    )

    class Meta:
        verbose_name = _("Акция")
        verbose_name_plural = _("Акции")

    def __str__(self):
        return self.name


class ProductPromotion(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Товар")
    )
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        verbose_name=_("Акция")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата добавления")
    )

    class Meta:
        verbose_name = _("Товар в акции")
        verbose_name_plural = _("Товары в акциях")

    def __str__(self):
        return f"{self.product.name} в {self.promotion.name}"