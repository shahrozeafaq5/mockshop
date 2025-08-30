# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from decimal import Decimal, InvalidOperation
from django.views.decorators.http import require_POST
from django.utils.html import escape

def product_list(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {})
    return render(request, 'shop/product_list.html', {'products': products, 'cart': cart})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    return render(request, 'shop/product_detail.html', {'product': product, 'cart': cart})

def _clean_qty(raw, default=1, min_v=1, max_v=100):
    try:
        q = int(raw)
        if q < min_v: return default
        if q > max_v: return max_v
        return q
    except (TypeError, ValueError):
        return default

@require_POST
def add_to_cart(request, product_id):
    qty = _clean_qty(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    key = str(int(product_id))  # normalize
    cart[key] = cart.get(key, 0) + qty
    request.session['cart'] = cart
    return redirect('product_detail', product_id=product_id)

@require_POST
def update_cart(request, product_id):
    qty = _clean_qty(request.POST.get('quantity', 1), default=1)
    cart = request.session.get('cart', {})
    key = str(int(product_id))
    if qty > 0:
        cart[key] = qty
    else:
        cart.pop(key, None)
    request.session['cart'] = cart
    return redirect('cart_view')

@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(int(product_id)), None)
    request.session['cart'] = cart
    return redirect('cart_view')

def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0.00')
    for pid, quantity in cart.items():
        product = get_object_or_404(Product, id=int(pid))
        q = _clean_qty(quantity)
        subtotal = product.price * q
        total += subtotal
        items.append({'product': product, 'quantity': q, 'subtotal': subtotal})
    return render(request, 'shop/cart.html', {'cart_items': items, 'total': total, 'cart': cart})

def checkout(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0.00')
    for pid, quantity in cart.items():
        product = get_object_or_404(Product, id=int(pid))
        q = _clean_qty(quantity)
        subtotal = product.price * q
        total += subtotal
        items.append({'product': product, 'quantity': q, 'subtotal': subtotal})

    if request.method == 'POST':
        name = (request.POST.get('name') or '').strip()
        email = (request.POST.get('email') or '').strip()
        address = (request.POST.get('address') or '').strip()

        if name and email and address and items:
            order = Order.objects.create(
                customer_name=name[:200],
                customer_email=email[:254],
                customer_address=address[:500],
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
