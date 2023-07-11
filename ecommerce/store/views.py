from django.forms import ModelForm
from django.http import JsonResponse
from django.conf import settings
from django.views import View
import json
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    TemplateView,
    RedirectView,
    ArchiveIndexView,
    YearArchiveView,
    DetailView,
    FormView,
    GenericViewError,
)


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email"]


# Function Based Views


@login_required
def customer_create_view(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            return redirect("/cart")
    else:
        form = CustomerForm()
    return render(
        request,
        os.path.join(settings.BASE_DIR, "templates/store/create_customer_FBW.html"),
        {"form": form},
    )


@login_required
def customer_delete_view(request, name):
    customer = get_object_or_404(Customer, name=name)
    if request.method == "POST":
        customer.delete()
        return redirect("/cart")
    return render(
        request,
        os.path.join(settings.BASE_DIR, "templates/store/delete_customer_FBW.html"),
        {"customer": customer},
    )


@login_required
def customer_update_view(request, name):
    customer = get_object_or_404(Customer, name=name)
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = CustomerForm()
    return render(
        request,
        os.path.join(settings.BASE_DIR, "templates/store/update_customer_FBW.html"),
        {"customer": customer, "form": form},
    )


def customer_view(request, customer_id=None, customer_name=None):
    if customer_name is not None:
        customer = get_object_or_404(Customer, pk=customer_id)
    elif customer_name is not None:
        customer = get_object_or_404(Customer, name=customer_name)
    else:
        customer = None
    # if customer_name is None :
    #     customer = Customer()

    if request.method == "POST":
        if customer is not None:
            form = CustomerForm(request.POST, instance=customer)
        else:
            form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("cart")
    else:
        if customer is not None:
            form = CustomerForm(instance=customer)
        else:
            form = CustomerForm()

    context = {
        "customer": customer,
        "form": form,
    }
    return render(
        request,
        os.path.join(settings.BASE_DIR, "templates/store/customer_FBW.html"),
        context,
    )


# Class Based Views
class StoreView(View):
    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False
            )
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
            cartItems = order["get_cart_items"]
        products = Product.objects.all()
        context = {"products": products, "cartItems": cartItems}
        print(
            "The path is: ",
            os.path.join(settings.BASE_DIR, "templates/store/checkout.html"),
        )
        return render(
            request,
            os.path.join(settings.BASE_DIR, "templates/store/store.html"),
            context,
        )


class CartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False
            )
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
            cartItems = order["get_cart_items"]
        context = {"items": items, "order": order, "cartItems": cartItems}
        return render(
            request,
            os.path.join(settings.BASE_DIR, "templates/store/cart.html"),
            context,
        )


class CheckoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False
            )
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
            cartItems = order["get_cart_items"]
        context = {"items": items, "order": order, "cartItems": cartItems}

        return render(
            request,
            os.path.join(settings.BASE_DIR, "templates/store/checkout.html"),
            context,
        )


class CustomerCreateView(CreateView):
    model = Customer
    fields = ["name", "email"]
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/customer_create.html"
    )
    success_url = "/cart"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/customer_delete.html"
    )
    success_url = "/cart"

    def get_object(self, queryset=None):
        name = self.kwargs["name"]
        return Customer.objects.get(name=name)


class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ["name", "email"]
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/update_customer.html"
    )
    success_url = "/"

    def get_object(self, queryset=None):
        name = self.kwargs["name"]
        return Customer.objects.get(name=name)


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "price", "digital", "image"]
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/product_create.html"
    )
    success_url = ""

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductListView(GenericViewError, ListView):
    model = Product
    template_name = os.path.join(settings.BASE_DIR, "templates/store/product_list.html")
    context_object_name = "products"


class ProductUpdateView(UpdateView):
    model = Product
    fields = ["price"]
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/update_product.html"
    )
    success_url = "/product_list"

    def get_object(self, queryset=None):
        name = self.kwargs["name"]
        return Product.objects.get(name=name)


class TemplateHomeView(TemplateView):
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/home_template.html"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OrderArchiveView(ArchiveIndexView):
    model = Order
    date_field = "date_ordered"
    allow_empty = True
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/order_archive.html"
    )
    paginate_by = 10


class UpdateItem(RedirectView):
    pattern_name = "cart"

    def post(self, request):
        data = json.loads(request.body)
        productId = data["productId"]
        action = data["action"]
        print("Action ", action)
        print("ProductId ", productId)

        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(
            order=order, product=product
        )

        if action == "add":
            orderItem.quantity = orderItem.quantity + 1
        elif action == "remove":
            orderItem.quantity = orderItem.quantity - 1

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse("Item was added", safe=False)


class ProductDetailView(DetailView):
    model = Product
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/product_detail.html"
    )
    context_object_name = "product"


class OrderItemCreateView(FormView):
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/orderitem_create.html"
    )
    success_url = "/cart"

    class OrderItemForm(ModelForm):
        class Meta:
            model = OrderItem
            fields = ["quantity", "order"]

    form_class = OrderItemForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class OrderDayArchiveView(YearArchiveView):
    model = Order
    date_field = "date_ordered"
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/orderday_archive.html"
    )
