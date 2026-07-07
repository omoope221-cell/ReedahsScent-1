from django import forms
from store.models import Product, Category
from orders.models import Order

TAILWIND_INPUT = 'w-full border border-stone-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#c8a97e] focus:border-transparent'


class StyledFormMixin:
    """Applies consistent Tailwind styling to every field automatically."""
    def style_fields(self):
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({'class': 'h-4 w-4 accent-[#1c1712]'})
            elif isinstance(widget, forms.Select):
                widget.attrs.update({'class': TAILWIND_INPUT})
            elif isinstance(widget, forms.Textarea):
                widget.attrs.update({'class': TAILWIND_INPUT, 'rows': 4})
            else:
                widget.attrs.update({'class': TAILWIND_INPUT})


class ProductForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'brand', 'fragrance_notes', 'description',
            'price', 'discount_price', 'image', 'stock', 'is_active', 'is_featured',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()


class CategoryForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()


class OrderStatusForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()
