from uuid import uuid4
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from .managers import *
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

users = User.objects.all()


class GenerateProfileImagePath(object):
    def __init__(self):
        pass


class TimestampModel(models.Model):
    created_at = models.DateTimeField()
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

    def save(self, *args, **kwargs):
        self.created_at = timezone.now()
        super(TimestampModel, self).save(*args, **kwargs)


class Customer(TimestampModel):
    gender_choices = [
        ("MALE", "Male"),
        ("FEMALE", "Female"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=50, choices=gender_choices, default="Male")
    orders = models.ManyToManyField(
        "Order", through="CustomerOrderHistory", related_name="orders_in_customer"
    )
    slug = models.SlugField(max_length=255, default="")

    def generate_slug(self):
        """Generates a unique slug for a customer."""
        slug = uuid4().hex[:20]
        while Customer.objects.filter(slug=slug).exists():
            slug = uuid4().hex[:20]
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_customer_order_first_timehistory(self):
        orders_customer_list = list(self.orders.all())
        history_order_list = []
        for each_order in orders_customer_list:
            history_order_list.append(
                each_order.order_in_customer_order_history.get().customer_order_created_at
            )

        return history_order_list

    def get_absolute_url(self):
        return reverse("detail_customer", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    def order_by_many(self):
        # return ",".join([str(o) for o in User.objects.all()])
        return self.user

    class Meta:
        app_label = "store"


class ProxyCustomer(Customer):
    customers = CustomerManager()

    class Meta:
        proxy = True
        ordering = ["name"]


class Product(TimestampModel):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(upload_to="", null=True, blank=True)

    objects = models.Manager()
    products = ProductManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={"pk": self.pk})

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(TimestampModel):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="customer_in_order",
    )
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    products = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="product_in_order",
    )
    created_by = users[0]

    objects = models.Manager()
    orders = OrderManager()

    def get_customer_order_created_at(self):
        customer_order_history = CustomerOrderHistory.objects.filter(order=self).first()
        if customer_order_history is not None:
            return customer_order_history.customer_order_created_at
        else:
            return None

    def __str__(self):
        return str(self.transaction_id)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.get("request", None)
        if self.request:
            self.created_by = self.request.user

    # def get_absolute_url(self):
    #     return reverse('order_detail', kwargs= {'pk':self.pk})

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

    # def __str__(self):
    #     return self.quantity


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
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_in_customer_order_history"
    )

    customer_order_created_at = models.DateTimeField(auto_now_add=True)


@receiver(pre_delete, sender=Order)
def delete_order_items(sender, instance, **kwargs):
    order_items = OrderItem.objects.filter(order=instance)
    order_items.delete()
    print("Order deleted by signal")


@receiver(post_save, sender=Order)
def add_order_items(sender, instance, **kwargs):
    order_items = OrderItem.objects.create(order=instance, product=instance.products)
    order_items.save()
    print("I'm inside add_order_items")


@receiver(pre_save, sender=Product)
def update_product(sender, instance, **kwargs):
    order = Order.objects.filter(products=instance)
    if order:
        print("Inside order, (pre_save)")
        order.products = instance
    print("I am in pre-save signal")


@receiver(post_delete, sender=CustomerOrderHistory)
def delete_order_history(sender, instance, **kwargs):
    order = Order.objects.get(transaction_id=instance.order.transaction_id)
    order.delete()
    print("Order history deleted by signal")


from django.contrib.sites.models import Site

class Site(models.Model):
    domain = models.CharField(max_length=100)
    verbose_name = models.CharField(max_length=100)

    def __str__(self):
        return self.domain

def create_site():
    site = Site(
        domain='localhost:8000/feed',
        verbose_name='store',
    )
    site.save()

if __name__ == '__main__':
    create_site()
