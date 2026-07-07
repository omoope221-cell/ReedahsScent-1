from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, Count, Q
from django.shortcuts import render, redirect, get_object_or_404

from store.models import Product, Category
from orders.models import Order
from .forms import ProductForm, CategoryForm, OrderStatusForm

LOW_STOCK_THRESHOLD = 5


def is_store_staff(user):
    return user.is_authenticated and user.is_active and user.is_staff


# ---------- Auth ----------

def dashboard_login(request):
    if is_store_staff(request.user):
        return redirect('dashboard:home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None and is_store_staff(user):
            login(request, user)
            return redirect('dashboard:home')
        messages.error(request, 'Invalid credentials, or this account does not have admin access.')

    return render(request, 'dashboard/login.html')


def dashboard_logout(request):
    logout(request)
    return redirect('dashboard:login')


# ---------- Dashboard home ----------

@user_passes_test(is_store_staff, login_url='dashboard:login')
def dashboard_home(request):
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(stock__lte=LOW_STOCK_THRESHOLD, is_active=True).order_by('stock')
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status=Order.STATUS_PENDING).count()
    confirmed_or_later = Order.objects.exclude(status__in=[Order.STATUS_PENDING, Order.STATUS_CANCELLED])
    total_revenue = sum(order.get_total_cost() for order in confirmed_or_later)
    recent_orders = Order.objects.all()[:6]

    return render(request, 'dashboard/home.html', {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
    })


# ---------- Products ----------

@user_passes_test(is_store_staff, login_url='dashboard:login')
def product_list(request):
    products = Product.objects.select_related('category').all()
    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(brand__icontains=query))
    return render(request, 'dashboard/product_list.html', {'products': products, 'query': query or ''})


@user_passes_test(is_store_staff, login_url='dashboard:login')
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added.')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm()
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Add Product'})


@user_passes_test(is_store_staff, login_url='dashboard:login')
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated.')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': f'Edit {product.name}', 'product': product})


@user_passes_test(is_store_staff, login_url='dashboard:login')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted.')
        return redirect('dashboard:product_list')
    return render(request, 'dashboard/confirm_delete.html', {'object': product, 'type_label': 'product'})


# ---------- Categories ----------

@user_passes_test(is_store_staff, login_url='dashboard:login')
def category_list(request):
    categories = Category.objects.annotate(product_count=Count('products'))
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added.')
            return redirect('dashboard:category_list')
    return render(request, 'dashboard/category_list.html', {'categories': categories, 'form': form})


@user_passes_test(is_store_staff, login_url='dashboard:login')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('dashboard:category_list')
    return render(request, 'dashboard/confirm_delete.html', {'object': category, 'type_label': 'category'})


# ---------- Orders ----------

@user_passes_test(is_store_staff, login_url='dashboard:login')
def order_list(request):
    orders = Order.objects.all()
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    return render(request, 'dashboard/order_list.html', {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'current_status': status or '',
    })


@user_passes_test(is_store_staff, login_url='dashboard:login')
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f'Order #{order.id} status updated to {order.get_status_display()}.')
            return redirect('dashboard:order_detail', pk=order.pk)
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'dashboard/order_detail.html', {'order': order, 'form': form})
