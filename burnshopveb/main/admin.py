from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, OrderItem, Review, Wishlist, Promotion, ProductPromotion

# Inline для OrderItem (вложенные элементы заказов)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('product', 'quantity', 'price', 'created_at')
    readonly_fields = ('created_at',)

# Inline для ProductPromotion (вложенные акции для товаров)
class ProductPromotionInline(admin.TabularInline):
    model = ProductPromotion
    extra = 1
    fields = ('promotion', 'created_at')
    readonly_fields = ('created_at',)

# Админ-класс для Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'discount_price', 'stock_status', 'created_at')
    list_filter = ('category', 'brand', 'created_at')
    inlines = [ProductPromotionInline]
    date_hierarchy = 'created_at'
    list_display_links = ('name',)
    raw_id_fields = ('category',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name', 'brand', 'description')

    @admin.display(description="Статус на складе")
    def stock_status(self, obj):
        return "В наличии" if obj.stock > 0 else "Нет в наличии"

# Админ-класс для Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at', 'formatted_delivery_address')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    list_display_links = ('id',)
    raw_id_fields = ('user',)
    readonly_fields = ('created_at', 'updated_at', 'total_amount')
    search_fields = ('user__username', 'status', 'delivery_address')

    @admin.display(description="Адрес доставки")
    def formatted_delivery_address(self, obj):
        return format_html("<pre>{}</pre>", obj.delivery_address)

# Админ-класс для Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at')
    list_filter = ('parent', 'created_at')
    date_hierarchy = 'created_at'
    list_display_links = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name',)

# Админ-класс для Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at', 'is_recent')
    list_filter = ('rating', 'created_at')
    date_hierarchy = 'created_at'
    list_display_links = ('product',)
    raw_id_fields = ('user', 'product')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('comment', 'user__username', 'product__name')

    @admin.display(description="Недавний?")
    def is_recent(self, obj):
        from datetime import timedelta
        from django.utils import timezone
        return timezone.now() - obj.created_at < timedelta(days=7)

# Админ-класс для Wishlist
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    list_display_links = ('product',)
    raw_id_fields = ('user', 'product')
    readonly_fields = ('created_at',)
    search_fields = ('user__username', 'product__name')

# Админ-класс для Promotion
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_percentage', 'start_date', 'end_date', 'is_active')
    list_filter = ('start_date', 'end_date')
    date_hierarchy = 'start_date'
    list_display_links = ('name',)
    readonly_fields = ('created_at',)
    search_fields = ('name',)

    @admin.display(description="Активна?")
    def is_active(self, obj):
        from django.utils import timezone
        return obj.start_date <= timezone.now() <= obj.end_date

# Админ-класс для ProductPromotion (связь многие-ко-многим)
@admin.register(ProductPromotion)
class ProductPromotionAdmin(admin.ModelAdmin):
    list_display = ('product', 'promotion', 'created_at')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    list_display_links = ('product',)
    raw_id_fields = ('product', 'promotion')
    readonly_fields = ('created_at',)
    search_fields = ('product__name', 'promotion__name')