from urllib.parse import quote
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem


def build_whatsapp_message(order, cart):
    """Builds the pre-filled WhatsApp message the customer sends to place the order."""
    lines = ["Hi Reedah's Scent! I would love to get this:", ""]

    for item in cart:
        lines.append(f"- {item['product'].name} x{item['quantity']} — ₦{item['total_price']}")

    lines += [
        "",
        f"Total: ₦{order.get_total_cost()}",
        "",
        f"Name: {order.full_name}",
        f"Phone: {order.phone_number}",
        f"Delivery Address: {order.address}, {order.city}, {order.state}",
        "",
        "Please confirm my order. I'll make payment to:",
        f"Account Number: {settings.STORE_ACCOUNT_NUMBER}",
        f"Bank: {settings.STORE_BANK_NAME}",
        f"Account Name: {settings.STORE_ACCOUNT_NAME}",
    ]
    return "\n".join(lines)


def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )

            message = build_whatsapp_message(order, cart)
            whatsapp_url = f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={quote(message)}"

            cart.clear()
            return redirect(whatsapp_url)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['full_name'] = request.user.get_full_name() or request.user.username
            initial['email'] = request.user.email
        form = OrderCreateForm(initial=initial)

    return render(request, 'orders/create.html', {'cart': cart, 'form': form})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/history.html', {'orders': orders})
