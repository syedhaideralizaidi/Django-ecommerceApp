from django.core.exceptions import ValidationError
from django.forms import (
    ModelForm,
    inlineformset_factory,
    modelformset_factory,
    ModelChoiceField,
)

from .models import Customer, Order, Product, CustomerOrderHistory


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email", "gender"]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        name = cleaned_data.get("name")
        if email and not email.endswith("@gmail.com"):
            raise ValidationError(
                "Please enter a valid email address ending with @gmail.com"
            )
        if len(name) < 10:
            raise ValidationError("Please enter more then 10 characters in Name field")


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "digital", "image"]


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["products", "transaction_id", "complete"]

    def save(self, commit=True):
        order = super().save(commit=False)
        if commit:
            order.save()
            self.save_m2m()
        return order


OrderFormset = inlineformset_factory(
    Customer,
    Order,
    form=OrderForm,
    extra=0,
    can_delete=True,
    validate_min=True,
)

CustomerOrderHistoryFormSet = inlineformset_factory(
    Customer, CustomerOrderHistory, fields=("order",), extra=2, can_delete=True
)

OrderTestFormset = modelformset_factory(
    Order,
    fields=(
        "products",
        "transaction_id",
        "complete",
    ),
    extra=1,
)
