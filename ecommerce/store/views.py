from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views import View
import json
import os
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    TemplateView,
    RedirectView,
)

# Create your views here.

from .models import *


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


class ProductListView(ListView):
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


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/customer_delete.html"
    )
    success_url = "/cart"

    def get_object(self, queryset=None):
        name = self.kwargs["name"]
        return Customer.objects.get(name=name)


class TemplateHomeView(TemplateView):
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/home_template.html"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
