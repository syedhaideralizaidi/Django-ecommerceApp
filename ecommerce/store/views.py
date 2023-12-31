import json
import os
from datetime import timedelta, datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponse,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import View
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

from .forms import CustomerForm, OrderCreateForm, OrderEditForm, OrderDeleteForm

from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext

from store.models import Customer, Product, Order, OrderItem


# Function Based Views


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.success(request, ("There was an error logging in, Try Again!"))
            return render(
                request,
                os.path.join(settings.BASE_DIR, "templates/store/invalid_action.html"),
            )
    else:
        return render(
            request, os.path.join(settings.BASE_DIR, "templates/store/login.html"), {}
        )


def logout_user(request):
    logout(request)
    return redirect("/")


@login_required
def customer_create_view(request):
    try:
        if request.method == "POST":
            form = CustomerForm(request.POST)
            if form.is_valid():
                customer = form.save(commit=False)
                customer.created_by = request.user
                customer.save()
                # return redirect("/cart")
                return redirect(f"{customer.name}/")
        else:
            form = CustomerForm()
        return render(
            request,
            os.path.join(settings.BASE_DIR, "templates/store/create_customer_FBW.html"),
            {"form": form},
        )
    except Exception as e:
        template = loader.get_template(
            os.path.join(settings.BASE_DIR, "templates/store/invalid_action.html")
        )
        return HttpResponse(template.render({}, request))


@login_required
def customer_delete_view(request, name):
    try:
        customer = get_object_or_404(Customer, name=name)
        if request.method == "POST":
            customer.delete()
            return redirect("/cart")
        return render(
            request,
            os.path.join(settings.BASE_DIR, "templates/store/delete_customer_FBW.html"),
            {"customer": customer},
        )
    except Exception as e:
        template = loader.get_template(
            os.path.join(settings.BASE_DIR, "templates/store/invalid_action.html")
        )
        return HttpResponse(template.render({}, request))


@login_required
def customer_update_view(request, name):
    try:
        customer = get_object_or_404(Customer, name=name)
        if request.method == "POST":
            form = CustomerForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("delete/")
        else:
            form = CustomerForm()
        return render(
            request,
            os.path.join(settings.BASE_DIR, "templates/store/update_customer_FBW.html"),
            {"customer": customer, "form": form},
        )
    except Exception as e:
        template = loader.get_template(
            os.path.join(settings.BASE_DIR, "templates/store/invalid_action.html")
        )
        return HttpResponse(template.render({}, request))


def customer_view(request, customer_name=None):
    if customer_name is None:
        customer_create_view(request)
    elif customer_name is not None:
        customer_update_view(request, customer_name)
    elif request.method == "GET":
        customer_delete_view(request, customer_name)


def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        text = gettext("Welcome to Our Store, What do you want to buy?")
    finally:
        activate(cur_language)
    return text
# Class Based Views
class StoreView(View):
    def get(self, request):
        trans = translate(language= 'fr')
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
        translated_products = [_(product.name) for product in products]
        obj = {
            "title": _("My Store"),
            "description": _("Welcome to Our Store, What do you want to buy?"),
        }
        context = {"products": products, "cartItems": cartItems, "meta": obj, "trans":trans}
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
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/customer_create.html"
    )

    form_class = CustomerForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        try:
            customer_name = self.object.name
            return f"customer_/{customer_name}"
        except Exception as e:
            template = loader.get_template(
                os.path.join(settings.BASE_DIR, "templates/store/invalid_action.html")
            )
            return HttpResponse(template.render({}, self.request))

    # def get_context_data(self , **kwargs) :
    #     context = super().get_context_data(**kwargs)
    #     context[ "orders_formset" ] = self.form_class.orders_formset(instance = self.object)
    #     return context

    def get_formset(self):
        formset = super().get_formset()
        formset.fields["orders"].queryset = self.request.user.orders.all()
        return formset


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/customer_confirm_delete.html"
    )
    success_url = "/"

    def get_object(self, queryset=None):
        try:
            pk = self.kwargs["pk"]
            print(pk)
            return Customer.objects.get(pk=pk)
        except Exception as e:
            template = loader.get_template(
                os.path.join(settings.BASE_DIR, "templates/store/invalid_action.html")
            )
            return HttpResponse(template.render({}, self.request))


class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ["name", "email"]
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/update_customer.html"
    )

    def get_object(self, queryset=None):
        name = self.kwargs["name"]
        try:
            return Customer.objects.get(name=name)
        except Customer.DoesNotExist:
            return render(
                self.request,
                os.path.join(settings.BASE_DIR, "templates/store/invalid_action.html"),
                {"status_code": 400},
            )

    def form_valid(self, form):
        try:
            form.save()
        except Exception as e:
            return HttpResponseBadRequest("An error occurred")

        return super().form_valid(form)

    def get_success_url(self):
        customer_name = self.object.name
        return f"/customer_/{customer_name}/delete"


class CustomerView(CreateView, ListView, UpdateView):
    model = Customer
    fields = ["name", "email"]
    template_name = os.path.join(settings.BASE_DIR, "templates/store/customer_FBW.html")

    def get_success_url(self):
        customer_name = self.object.name
        return f"customer_/{customer_name}"


class CheckView(DetailView, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "templates/store/customer_confirm_delete.html"

    def get_object(self, query_set=None):
        pk = self.kwargs["pk"]
        return Customer.objects.get(pk=pk)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("customer_delete", kwargs={"pk": pk})


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "price", "digital"]
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/product_create.html"
    )
    success_url = "/"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.image = self.request.FILES.get("image")
        return super().form_valid(form)


def change_timezone(product):
    product.created_at = product.created_at + timedelta(hours=0)


def test_timezone(product):
    return product.created_at + timedelta(hours=2)


def product_list(request):
    products = Product.objects.all()
    for product in products:
        change_timezone(product)
    return render(request, "store/product_list.html", {"products": products})


class ProductListView(GenericViewError, ListView):
    model = Product
    template_name = os.path.join(settings.BASE_DIR, "templates/store/product_list.html")
    context_object_name = "products"

    def get_queryset(self):
        products = super().get_queryset()
        for product in products:
            change_timezone(product)
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["five_hours_from_now"] = datetime.now() + timedelta(hours=5)
        return context


class CustomerListView(ListView):
    model = Customer
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/customer_list.html"
    )
    context_object_name = "customers"


class ProductUpdateView(UpdateView):
    model = Product
    fields = ["price", "image"]
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/update_product.html"
    )
    success_url = "/product_list"

    def get_object(self, queryset=None):
        name = self.kwargs["name"]
        return Product.objects.get(name=name)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = os.path.join(
        settings.BASE_DIR, "templates/store/product_delete.html"
    )
    success_url = "/"

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


class OrderCreateView(CreateView):
    template_name = "templates/store/order_form.html"
    form_class = OrderCreateForm
    model = Order
    # def get_success_url(self):
    #     order = self.object
    #     return f'order/{order.pk}/update'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class OrderUpdateView(UpdateView):
    template_name = "templates/store/order_update.html"
    form_class = OrderEditForm
    model = Order

    def get_success_url(self):
        order = self.object
        return f"/order/{order.pk}/delete"


class OrderDeleteView(DeleteView):
    model = Order
    form_class = OrderDeleteForm
    template_name = "templates/store/order_delete.html"
    success_url = "/order"

    def get_object(self, queryset=None):
        order_id = self.kwargs["pk"]
        try:
            return Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return render(
                self.request,
                "templates/store/invalid_action.html",
                {"status_code": 400},
            )
