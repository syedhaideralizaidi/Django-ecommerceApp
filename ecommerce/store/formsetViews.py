from django.contrib import messages
from django.http import HttpResponseRedirect , JsonResponse
from django.shortcuts import render , redirect
from django.urls import reverse
from django.views.generic import ListView , DetailView
from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import (
    CreateView , FormView
)

from .Formsetforms import CustomerOrderHistoryFormSet , OrderForm , CustomerForm
from .models import Customer


class HomeView(TemplateView):
    template_name = 'templates/store/fvhome.html'

class CustomersViewList(ListView):
    model = Customer
    template_name = 'templates/store/fvlist.html'
    context_object_name = 'customers'

class CustomersAddView(CreateView):
    model = Customer
    template_name = 'templates/store/fvadd.html'
    form_class = CustomerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['order_form'] = OrderForm(self.request.POST)
        else:
            context['order_form'] = OrderForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        order_form = context['order_form']

        if order_form.is_valid():
            self.object = form.save()
            order = order_form.save(commit=False)
            order.customer = self.object
            order.save()
            self.object.orders.add(order)
            return redirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'templates/store/fvdetail.html'

class CustomerOrderUpdateView(SingleObjectMixin, FormView):
    model = Customer
    template_name = 'templates/store/customer_order_update.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset = Customer.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset = Customer.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class = None) :
        return CustomerOrderHistoryFormSet(**self.get_form_kwargs(), instance = self.object)

    def form_valid(self , form):
        form.save()
        messages.add_message(
            self.request ,
            messages.SUCCESS ,
            'Changes were saved.'
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) :
        return reverse('detail_customer' , kwargs = {'pk' : self.object.pk})


def create_customer_ajax(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        gender = request.POST['gender']

        customer = Customer.objects.create(
            name=name, email=email, gender=gender
        )
        customer.save()
        return redirect('/')
    else:
        return render(request, 'templates/store/customer_ajax.html')

def validate(request):
    name = request.POST['name']
    data = {
        'taken' : Customer.objects.filter(name__iexact=name).exists()
    }
    return JsonResponse(data)


def get_customers(self):
    customers = Customer.objects.all()
    response = []
    for customer in customers:
        response.append({
            'name': customer.name,
            'email': customer.email,
        })
    return JsonResponse({'customers': response})


# class CustomersAddView(CreateView):
#     model = Customer
#     template_name = 'templates/store/fvadd.html'
#     fields = '__all__'
#
#     def form_valid(self, form):
#         self.object = form.save()
#         order_pk = self.object.pk
#         return redirect(f'/fvhome/{order_pk}')

# class CustomersAddView(CreateView):
#     model = Customer
#     template_name = 'templates/store/fvadd.html'
#     form_class = CustomerForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context['order_form'] = OrderForm(self.request.POST)
#             context['order_history_formset'] = CustomerOrderHistoryFormSet(self.request.POST, instance=self.object)
#         else:
#             context['order_form'] = OrderForm()
#             context['order_history_formset'] = CustomerOrderHistoryFormSet(instance=self.object)
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         order_form = context['order_form']
#         order_history_formset = context['order_history_formset']
#
#         if order_form.is_valid() and order_history_formset.is_valid():
#             self.object = form.save()
#             order = order_form.save(commit=False)
#             order.customer = self.object
#             order.save()
#             order_history_formset.instance = self.object
#             order_history_formset.save()
#             return redirect(f'/fvhome/{self.object.pk}')
#         else:
#             print("What happened")
#             return self.render_to_response(self.get_context_data(form=form))

