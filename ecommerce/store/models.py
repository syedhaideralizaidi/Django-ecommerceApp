from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils import timezone

users = User.objects.all()


class TimestampModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created_by",
        default=1,
    )

    class Meta:
        abstract = True


class Customer(TimestampModel):
    class Gender(models.TextField):
        MALE = "ML", "Male"
        FEMALE = "FL", "Female"

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    gender = models.CharField(
        max_length=50, choices=[Gender.MALE, Gender.FEMALE], default=Gender.MALE
    )
    orders = models.ManyToManyField(
        "Order", blank=True, related_name="%(class)s_orders"
    )

    # def get_absolute_url(self) :
    #     return reverse("checkc_" , kwargs = {"slug" : self.slug})

    def __str__(self):
        return self.name

    def order_by_many(self):
        # return ",".join([str(o) for o in User.objects.all()])
        return self.user


class Product(TimestampModel):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(TimestampModel):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.complete)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
            return shipping


class OrderItem(TimestampModel):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return self.quantity


class ShippingAddress(TimestampModel):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class CustomerOrderHistory(TimestampModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer} placed order {self.order} on {self.created_at}"


@receiver(m2m_changed, sender=Customer.orders.through)
def create_customer_order_history(
    sender, instance, action, reverse, model, pk_set, **kwargs
):
    if action == "post_add" and not reverse and model == Order:
        for order_id in pk_set:
            history = CustomerOrderHistory.objects.create(
                customer=instance, order_id=order_id, created_by=instance.user
            )
