from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:category_detail', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    brand = models.CharField(max_length=120, blank=True, help_text="e.g. Reedah's Scent")
    fragrance_notes = models.CharField(max_length=255, blank=True, help_text="e.g. Vanilla, Oud, Amber")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in Naira (₦)")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    @property
    def current_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def in_stock(self):
        return self.stock > 0


class ProductImage(models.Model):
    """Extra gallery images for a product."""
    product = models.ForeignKey(Product, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"Image for {self.product.name}"
