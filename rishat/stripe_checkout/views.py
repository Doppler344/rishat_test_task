from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse

from .models import Item, Order, OrderSet

import stripe

from rishat.settings import STRIPE_SECRET_KEY, STRIPE_PUBLIC_KEY


@require_http_methods(["GET"])
def get_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'item.html', {'item': item, 'stripe_public_key': STRIPE_PUBLIC_KEY})


@require_http_methods(["GET"])
def buy_item(request, item_id):
    stripe.api_key = STRIPE_SECRET_KEY
    item = get_object_or_404(Item, id=item_id)
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),  # because of cents * 100
            },
            'quantity': 1,
        }, ],
        mode='payment',
        success_url='http://127.0.0.1:8000/success',
        cancel_url='http://127.0.0.1:8000/cancel',
    )

    return JsonResponse({'id': session.id})


@require_http_methods(["GET"])
def get_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order.html', {'order': order, 'items': get_list_or_404(OrderSet, order_id=order.pk),
                                          'stripe_public_key': STRIPE_PUBLIC_KEY})


@require_http_methods(["GET"])
def buy_order(request, order_id):
    stripe.api_key = STRIPE_SECRET_KEY
    order = get_object_or_404(Order, id=order_id)
    discount_amount = order.discount_id.amount * 100  # because of %
    tax_amount = order.tax_id.amount * 100  # because of %
    discount = stripe.Coupon.create(percent_off=discount_amount, duration="once")
    tax = stripe.TaxRate.create(
        display_name=order.tax_id.taxation_name,
        inclusive=False,
        percentage=tax_amount,
        country="US",
        state="CA",
        jurisdiction="US - CA",
        description="CA Sales Tax",
    )
    order_sets = get_list_or_404(OrderSet, order_id=order_id)
    items = []
    for order_set in order_sets:
        items.append({
            'price_data': {
                'currency': order_set.item_id.currency,
                'product_data': {
                    'name': order_set.item_id.name,
                },
                'unit_amount': int(order_set.item_id.price * 100),  # because of cents * 100
            },
            'quantity': order_set.amount,
            "tax_rates": [tax.id, ],
        }, )
    session = stripe.checkout.Session.create(
        line_items=items,
        mode='payment',
        discounts=[{'coupon': discount.id}, ],
        success_url='http://127.0.0.1:8000/success',
        cancel_url='http://127.0.0.1:8000/cancel',
    )

    return JsonResponse({'id': session.id})


@require_http_methods(["GET"])
def success(request):
    return HttpResponse("success")


@require_http_methods(["GET"])
def cancel(request):
    return HttpResponse("cancel")


@require_http_methods(["GET"])
def index(request):
    items = get_list_or_404(Item)
    orders = get_list_or_404(Order)
    orders_with_set = []
    for order in orders:
        orders_with_set.append({'order': order, 'items': get_list_or_404(OrderSet, order_id=order.pk)})
    return render(request, 'index.html', {'items_list': items, 'orders_with_set_list': orders_with_set})
