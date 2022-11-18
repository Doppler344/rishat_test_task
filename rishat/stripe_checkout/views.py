from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from .models import Item

import stripe

from rishat.settings import STRIPE_SECRET_KEY, STRIPE_PUBLIC_KEY


@require_http_methods(["GET"])
def get_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'main_item.html', {'item': item, 'stripe_public_key': STRIPE_PUBLIC_KEY})


@require_http_methods(["GET"])
def buy_item(request, item_id):
    stripe.api_key = STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'USD',
                'product_data': {
                    'name': 'T-shirt',
                },
                'unit_amount': 20000,
            },
            'quantity': 11,
        }, {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Tort',
                },
                'unit_amount': 30,
            },
            'quantity': 11,
        }],
        mode='payment',
        success_url='http://localhost:8080/success',
        cancel_url='http://localhost:8080/cancel',
    )
    item = get_object_or_404(Item, id=item_id)
    return JsonResponse({'id': session.id})
