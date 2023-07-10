from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views import View
import json
import os

# Create your views here.
print(os.getcwd())
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


class UpdateItem(View):
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
