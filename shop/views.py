from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.html import escape
from .models import Product, Order, OrderItem


def product_list(request):
    products = Product.objects.all()
    return render(request, "shop/product_list.html", {"products": products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "shop/product_detail.html", {"product": product})


def cart_view(request):
    order = None
    order_id = request.session.get("cart_order_id")
    if order_id:
        order = Order.objects.filter(id=order_id).first()
    return render(request, "shop/cart.html", {"order": order})


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # 🔒 Validate quantity strictly
    quantity_raw = request.POST.get("quantity", "1")
    if not quantity_raw.isdigit():
        messages.error(request, "Invalid quantity format.")
        return redirect("product_detail", product_id=product.id)

    quantity = int(quantity_raw)
    if quantity < 1 or quantity > 10:
        messages.error(request, "Quantity must be between 1 and 10.")
        return redirect("product_detail", product_id=product.id)

    # Get/create order
    order_id = request.session.get("cart_order_id")
    if order_id:
        order = Order.objects.filter(id=order_id).first()
    else:
        order = Order.objects.create(
            customer_name="Guest",
            customer_email="guest@example.com",
            customer_address="N/A",
        )
        request.session["cart_order_id"] = order.id

    # Safe ORM (no raw SQL)
    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={"quantity": quantity, "price": product.price},
    )
    if not created:
        new_qty = min(order_item.quantity + quantity, 10)
        order_item.quantity = new_qty
        order_item.save()

    messages.success(request, f"{escape(product.name)} added to cart.")
    return redirect("cart_view")


@require_POST
def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order_id = request.session.get("cart_order_id")
    if not order_id:
        messages.error(request, "No active cart.")
        return redirect("cart_view")

    order = Order.objects.filter(id=order_id).first()
    if not order:
        messages.error(request, "Cart not found.")
        return redirect("cart_view")

    # 🔒 Validate quantity strictly
    quantity_raw = request.POST.get("quantity", "1")
    if not quantity_raw.isdigit():
        messages.error(request, "Invalid quantity format.")
        return redirect("cart_view")

    quantity = int(quantity_raw)
    if quantity < 1 or quantity > 10:
        messages.error(request, "Quantity must be between 1 and 10.")
        return redirect("cart_view")

    try:
        order_item = OrderItem.objects.get(order=order, product=product)
        order_item.quantity = quantity
        order_item.save()
        messages.success(request, f"Updated {escape(product.name)} quantity.")
    except OrderItem.DoesNotExist:
        messages.error(request, "Item not found in cart.")

    return redirect("cart_view")


@require_POST
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order_id = request.session.get("cart_order_id")
    if not order_id:
        messages.error(request, "No active cart.")
        return redirect("cart_view")

    order = Order.objects.filter(id=order_id).first()
    if not order:
        messages.error(request, "Cart not found.")
        return redirect("cart_view")

    try:
        order_item = OrderItem.objects.get(order=order, product=product)
        order_item.delete()
        messages.success(request, f"{escape(product.name)} removed from cart.")
    except OrderItem.DoesNotExist:
        messages.error(request, "Item not found in cart.")

    return redirect("cart_view")


def checkout(request):
    order_id = request.session.get("cart_order_id")
    order = None
    if order_id:
        order = Order.objects.filter(id=order_id).first()
    return render(request, "shop/checkout.html", {"order": order})
