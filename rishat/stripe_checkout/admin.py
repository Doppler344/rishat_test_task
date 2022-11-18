from django.contrib import admin

from .models import Item, Order, OrderSet, Tax, Discount


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'currency',)
    list_display_links = ('name',)
    search_fields = ('name', 'description',)


admin.site.register(Item, ItemAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_of_order', 'status', 'currency', 'tax_id', 'discount_id',)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderSet)


class TaxAdmin(admin.ModelAdmin):
    list_display = ('pk', 'taxation_name', 'amount',)


admin.site.register(Tax, TaxAdmin)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'discount_name', 'amount',)


admin.site.register(Discount, DiscountAdmin)
