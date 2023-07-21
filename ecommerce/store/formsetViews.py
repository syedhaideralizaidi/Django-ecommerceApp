from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, FormView

from .Formsetforms import (
    CustomerOrderHistoryFormSet,
    OrderForm,
    CustomerForm,
    OrderFormset,
    ProductForm,
    OrderTestFormset,
)
from .models import Customer, Order, CustomerOrderHistory, Product


class HomeView(TemplateView):
    template_name = "templates/store/fvhome.html"


class CustomersViewList(ListView):
    model = Customer
    template_name = "templates/store/fvlist.html"
    context_object_name = "customers"


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderFormset
    template_name = "templates/store/order_form.html"

    def form_valid(self, form):
        order = form.save()
        data = {
            "order_id": order.id,
            "order_label": str(order),
        }
        return JsonResponse(data)


class CustomerDetailView(DetailView):
    model = Customer
    template_name = "templates/store/fvdetail.html"


class CustomerOrderUpdateView(SingleObjectMixin, FormView):
    model = Customer
    template_name = "templates/store/customer_order_update.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Customer.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Customer.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return CustomerOrderHistoryFormSet(
            **self.get_form_kwargs(), instance=self.object
        )

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, "Changes were saved.")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("detail_customer", kwargs={"pk": self.object.pk})


def product_add_view(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    data = {}
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        if form.is_valid():
            form.save()
            data["name"] = form.cleaned_data.get("name")
            data["status"] = "ok"
            return JsonResponse(data)
            # return redirect('product_list')

    context = {"form": form}
    return render(request, "templates/store/newproduct_create.html", context)


def create_customer_ajax(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        gender = request.POST["gender"]

        customer = Customer.objects.create(name=name, email=email, gender=gender)
        customer.save()
        return redirect("/")
    else:
        return render(request, "templates/store/customer_ajax.html")


def validate(request):
    name = request.POST["name"]
    data = {"taken": Customer.objects.filter(name__iexact=name).exists()}
    return JsonResponse(data)


def get_customers(self):
    customers = Customer.objects.all()
    response = []
    for customer in customers:
        response.append(
            {
                "name": customer.name,
                "email": customer.email,
            }
        )
    return JsonResponse({"customers": response})


def add_order_form(request):
    form = OrderForm()
    form_num = request.GET.get("form_num")
    return render(
        request,
        "templates/store/order_form.html",
        {
            "form": form,
            "form_num": form_num,
        },
    )


def add_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            data = {
                "order_id": order.id,
                "order_label": str(order),
            }
            return JsonResponse(data)
        else:
            return JsonResponse({"error": "Form is not valid"})
    else:
        return JsonResponse({"error": "Invalid request method"})


def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = ProductForm()

    context = {
        "form": form,
    }

    return render(request, "templates/store/product_create.html", context)


def file_upload(request):
    file = request.FILES.get("file")
    fss = FileSystemStorage()
    filename = fss.save(file.name, file)
    url = fss.url(filename)
    product = Product.objects.filter(pk=request.pk)
    product.image = filename

    return JsonResponse({"link": url})

    # if request.method == 'POST':
    #     file = request.FILES["image"]
    #     fss = FileSystemStorage()
    #     filename = fss.save(file.name , file)
    #     name = request.POST["name"]
    #     price = request.POST["price"]
    #     product = Product.objects.create(image = filename , price = price , name = name)
    #     product.save()
    #     success = 'Profile Created Successfully'
    #     return HttpResponse(success)


class OrderAddView(TemplateView):
    template_name = "templates/store/orderadd_form.html"

    def get(self, *args, **kwargs):
        customer_form = CustomerForm()
        order_formset = OrderTestFormset(queryset=Order.objects.none())
        return self.render_to_response(
            {
                "customer_form": customer_form,
                "order_formset": order_formset,
            }
        )

    def post(self, *args, **kwargs):
        customer_form = CustomerForm(data=self.request.POST)
        order_formset = OrderTestFormset(data=self.request.POST)

        if customer_form.is_valid() and order_formset.is_valid():
            customer = customer_form.save()

            for order_form in order_formset:
                order = order_form.save(commit=False)
                order.customer = customer
                order.save()
                CustomerOrderHistory.objects.create(customer=customer, order=order)

            return redirect(f"/fvhome/{customer.pk}/")

        return self.render_to_response(
            {
                "customer_form": customer_form,
                "order_formset": order_formset,
            }
        )
