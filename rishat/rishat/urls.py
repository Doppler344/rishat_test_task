"""rishat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from stripe_checkout.views import get_item, buy_item, cancel, success, index, buy_order, get_order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('item/<int:item_id>/', get_item, name='item_list'),
    path('buy/<int:item_id>/', buy_item, name='buy_list'),
    path('order/<int:order_id>/', get_order, name='order_list'),
    path('buy_order/<int:order_id>/', buy_order, name='buy_order_list'),
    path('cancel', cancel, name='cancel'),
    path('success', success, name='success'),

]
