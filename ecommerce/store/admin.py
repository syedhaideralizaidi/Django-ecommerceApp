from django.contrib import admin
from django.shortcuts import redirect

from .models import Customer, Product, Order, OrderItem, ShippingAddress
from .models import *


class TimestampedModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created_by",)
    exclude = ("created_at", "updated_at")


@admin.register(Customer)
class CustomerAdmin(TimestampedModelAdmin):
    list_display = (
        "name",
        "email",
    )
    # list_display_links = ("name","email")
    exclude = ("user",)
    readonly_fields = ("created_at", "updated_at", "created_by")


@admin.register(Product)
class ProductAdmin(TimestampedModelAdmin):
    list_display = ("name", "price", "digital")

    actions = ["mark_as_digital"]

    def mark_as_digital(self, request, queryset):
        queryset.update(digital=True)


@admin.register(Order)
class OrderAdmin(TimestampedModelAdmin):
    list_display = ("transaction_id", "date_ordered", "complete")

    actions = ["mark_as_complete"]

    def mark_as_complete(self, request, queryset):
        queryset.update(complete=True)


@admin.register(OrderItem)
class OrderItemAdmin(TimestampedModelAdmin):
    list_display = ("quantity", "date_added", "order")


@admin.register(ShippingAddress)
class ShippingAddressAdmin(TimestampedModelAdmin):
    pass


@admin.register(CustomerOrderHistory)
class CustomerOrderHistoryAdmin(TimestampedModelAdmin):
    pass
