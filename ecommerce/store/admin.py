from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, ShippingAddress


class TimestampedModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")


@admin.register(Customer)
class CustomerAdmin(TimestampedModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(TimestampedModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(TimestampedModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(TimestampedModelAdmin):
    pass


@admin.register(ShippingAddress)
class ShippingAddressAdmin(TimestampedModelAdmin):
    pass
