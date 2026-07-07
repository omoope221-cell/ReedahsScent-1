from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_price', 'stock', 'is_active', 'is_featured', 'created_at')
    list_filter = ('category', 'is_active', 'is_featured')
    list_editable = ('price', 'discount_price', 'stock', 'is_active', 'is_featured')
    search_fields = ('name', 'brand', 'fragrance_notes')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
