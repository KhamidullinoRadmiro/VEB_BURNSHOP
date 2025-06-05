from django.contrib import admin
from .models import Category, Product, Promotion, Review, Wishlist

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock')
    raw_id_fields = ('category',)
    search_fields = ('name', 'brand', 'description')
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].widget.attrs['style'] = 'width: 700px;'
        return form

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_percentage', 'start_date', 'end_date')
    search_fields = ('name',)
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].widget.attrs['style'] = 'width: 700px;'
        return form

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    raw_id_fields = ('product', 'user')
    search_fields = ('product__name', 'user__username', 'comment')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    raw_id_fields = ('user', 'product')
    search_fields = ('user__username', 'product__name')