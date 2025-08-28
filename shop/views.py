from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from decimal import Decimal
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

def product_list(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {})
    return render(request, 'shop/product_list.html', {'products': products, 'cart': cart})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    return render(request, 'shop/product_detail.html', {'product': product, 'cart': cart})

@require_POST
def add_to_cart(request, product_id):
    qty = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + qty
    request.session['cart'] = cart
    return redirect('product_detail', product_id=product_id)

@require_POST
def update_cart(request, product_id):
    qty = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    key = str(product_id)
    if qty > 0:
        cart[key] = qty
    else:
        cart.pop(key, None)
    request.session['cart'] = cart
    return redirect('cart_view')

@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart_view')

def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0.00')
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        subtotal = product.price * int(quantity)
        total += subtotal
        items.append({'product': product, 'quantity': int(quantity), 'subtotal': subtotal})
    return render(request, 'shop/cart.html', {'cart_items': items, 'total': total, 'cart': cart})

@ratelimit(key='ip', rate='5/m', block=True)
def checkout(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0.00')
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        subtotal = product.price * int(quantity)
        total += subtotal
        items.append({'product': product, 'quantity': int(quantity), 'subtotal': subtotal})

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        if name and email and address and items:
            order = Order.objects.create(
                customer_name=name,
                customer_email=email,
                customer_address=address,
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price,
                )
            request.session['cart'] = {}
            return render(request, 'shop/checkout_success.html', {'order': order})

    return render(request, 'shop/checkout.html', {'items': items, 'total': total, 'cart': cart})
