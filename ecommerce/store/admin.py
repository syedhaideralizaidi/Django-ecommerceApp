from django import forms
from django.contrib import admin

from .models import *


class TimestampedModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created_by",)
    exclude = ("created_at", "updated_at")


class OrderInline(admin.TabularInline):
    model = Customer.orders.through

    # readonly_fields = ("order")


@admin.register(Customer)
class CustomerAdmin(TimestampedModelAdmin):
    list_display = (
        "name",
        "email",
    )
    # list_display_links = ("name","email")
    exclude = ("user",)
    inlines = [OrderInline]

    readonly_fields = ("created_at", "updated_at", "created_by")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["name"].label = "Customer Name"
        form.base_fields["email"].label = "Customer Email"
        return form

    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["title"] = "Hello, Please add New Customer"
        return super().add_view(request, form_url=form_url, extra_context=extra_context)


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "name",
            "price",
            "digital",
            "image",
            "created_by",
        )

    def clean_name(self):
        if any(c.isdigit() for c in self.cleaned_data["name"]):
            raise forms.ValidationError("The name should only be in string")
        # messages.error(self.request , "The message")
        return self.cleaned_data["name"]


@admin.register(Product)
class ProductAdmin(TimestampedModelAdmin):
    list_display = ("name", "price", "digital")

    actions = ["mark_as_digital"]

    list_filter = ("digital",)
    search_fields = ("name__startswith",)
    form = ProductAdminForm

    def mark_as_digital(self, request, queryset):
        queryset.update(digital=True)

    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["title"] = "Welcome, Please add New Product"
        return super().add_view(request, form_url=form_url, extra_context=extra_context)

    def get_form(self, request, obj=None, **kwargs):
        kwargs["widgets"] = {
            "name": forms.TextInput(
                attrs={"placeholder": "Enter Product Name e.g. Shoes"}
            ),
            "price": forms.TextInput(attrs={"placeholder": "Enter Price"}),
        }
        kwargs["labels"] = {
            "name": "Product Name",
            "price": "Product Price",
        }
        return super().get_form(request, obj, **kwargs)


@admin.register(Order)
class OrderAdmin(TimestampedModelAdmin):
    list_display = ("transaction_id", "date_ordered", "complete")

    readonly_fields = ("date_ordered", "created_at")

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
    list_display = ("customer", "order")
    readonly_fields = (
        "customer",
        "order",
        "customer_order_created_at",
    )
    exclude = ("created_by", "created_at")


@admin.register(ProxyCustomer)
class ProxyCustomerAdmin(TimestampedModelAdmin):
    list_display = (
        "name",
        "email",
    )
