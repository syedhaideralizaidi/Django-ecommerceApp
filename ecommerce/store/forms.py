from django.forms import (
    ModelForm,
    CheckboxSelectMultiple,
    ModelMultipleChoiceField,
    CharField,
    TextInput,
    DecimalField,
    NumberInput,
    BooleanField,
    CheckboxInput,
)

from .models import Customer, Order, Product


class CustomerForm(ModelForm):
    orders = ModelMultipleChoiceField(
        queryset=Order.objects.all(),
        required=False,
        label="Orders",
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = Customer
        fields = ["name", "email", "orders"]


class ProductForm(ModelForm):
    name = CharField(
        widget=TextInput(attrs={"id": "custom_name_id", "name": "custom_name"})
    )
    price = DecimalField(
        widget=NumberInput(attrs={"id": "custom_price_id", "price": "custom_price"})
    )
    digital = BooleanField(
        widget=CheckboxInput(
            attrs={"id": "custom_digital_id", "digital": "custom_digital"}
        )
    )

    class Meta:
        model = Product
        fields = ["name", "price", "digital"]


class OrderCreateForm(ModelForm):
    class Meta:
        model = Order
        fields = ["products", "customer", "complete", "transaction_id"]

    # OrderFormSet = inlineformset_factory(Customer , Order , form = OrderCreateForm, extra = 1)


class OrderEditForm(ModelForm):
    class Meta:
        model = Order
        fields = ["complete", "products"]


class OrderDeleteForm(ModelForm):
    class Meta:
        model = Order
        fields = []


# inlineformset_factory(Customer, Order, fields = ('complete','products',))
# orders_formset = inlineformset_factory(Customer , Order , fields = ('complete' , 'products' ,) , extra = 1)
