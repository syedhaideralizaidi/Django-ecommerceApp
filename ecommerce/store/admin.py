from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, ShippingAddress


class TimestampedModelAdmin(admin.ModelAdmin):
    readonly_fields=("created_by",)
    exclude = ("created_at" , "updated_at")


@admin.register(Customer)
class CustomerAdmin(TimestampedModelAdmin):
    list_display = ("name","email","order_by_many")
    # list_display_links = ("name","email")


@admin.register(Product)
class ProductAdmin(TimestampedModelAdmin):
    list_display = ("name","price","digital")


@admin.register(Order)
class OrderAdmin(TimestampedModelAdmin):
    list_display = ("transaction_id","date_ordered" , "complete")


@admin.register(OrderItem)
class OrderItemAdmin(TimestampedModelAdmin):
    list_display = ("quantity","date_added" , "order")


@admin.register(ShippingAddress)
class ShippingAddressAdmin(TimestampedModelAdmin):
    pass
