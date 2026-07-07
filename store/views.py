from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Category, Product
from cart.forms import CartAddProductForm


def home(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'categories': categories,
    })


def product_list(request):
    products = Product.objects.filter(is_active=True)
    category_slug = request.GET.get('category')
    query = request.GET.get('q')
    categories = Category.objects.all()
    current_category = None

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(brand__icontains=query) | Q(fragrance_notes__icontains=query)
        )

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'store/product_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': current_category,
        'query': query or '',
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'store/product_list.html', {
        'page_obj': Paginator(products, 12).get_page(request.GET.get('page')),
        'categories': Category.objects.all(),
        'current_category': category,
        'query': '',
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    cart_product_form = CartAddProductForm()
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'related_products': related_products,
    })
