from django.forms import ModelForm , inlineformset_factory

from .models import Customer , Order , CustomerOrderHistory


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name','email','gender']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['products', 'transaction_id','complete']

    # customers = ModelMultipleChoiceField(
    #     queryset = Customer.objects.all() ,
    #     widget = CheckboxSelectMultiple ,
    #     required = False ,
    # )

    # def __init__(self , *args , **kwargs) :
    #     super().__init__(*args , **kwargs)
    #     if self.instance.pk :
    #         self.fields[ 'customer' ].initial = self.instance.customer

    def save(self , commit = True) :
        order = super().save(commit = False)
        if commit :
            order.save()
            self.save_m2m()
        return order

CustomerOrderHistoryFormSet = inlineformset_factory(
    Customer, CustomerOrderHistory, fields=('order',), extra=3, can_delete=True
)

