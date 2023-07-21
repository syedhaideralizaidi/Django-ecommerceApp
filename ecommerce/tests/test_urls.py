import os

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, Client

from django.test import SimpleTestCase
from django.urls import reverse , resolve

from store.models import Product
from store.views import StoreView , CartView , login , CheckoutView , ProductUpdateView , ProductDetailView , \
    ProductDeleteView , login_user , logout_user
from store.formsetViews import product_add_view , HomeView , CustomersViewList , OrderAddView , CustomerDetailView , \
    CustomerOrderUpdateView , validate , create_customer_ajax


class TestUrls(SimpleTestCase):
    def test_StoreUrl(self):
        url = reverse('store')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, StoreView)

    def test_CartUrl(self):
        url = reverse('cart')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, CartView)

    def test_CheckoutUrl(self):
        url = reverse('checkout')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class , CheckoutView)

    def test_ProductUpdateUrl(self):
        url = reverse('product_update', args = ['Code'])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class , ProductUpdateView)

    def test_NewProductUrl(self):
        url = reverse('product_add_view')
        print(resolve(url))
        self.assertEquals(resolve(url).func, product_add_view)

    def test_ProductDetailUrl(self):
        url = reverse('product_detail', args = ['2'])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class , ProductDetailView)

    def test_ProductUpdateUrl(self):
        url = reverse('product_update', args = ['Shoes'])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, ProductUpdateView)
    def test_ProductDeleteUrl(self):
        url = reverse('product_delete', args = ['Shoes'])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, ProductDeleteView)

    def test_CustomerUrl(self):
        url = reverse('fvhome')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, HomeView)

    def test_CustomerListUrl(self):
        url = reverse('fvhome_customerlist')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, CustomersViewList)

    def test_CustomerAddUrl(self) :
        url = reverse('add_customer')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class , OrderAddView)

    def test_CustomerDetailUrl(self) :
        url = reverse('detail_customer', args = ['89'])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class , CustomerDetailView)

    def test_CustomerDetailUrl(self) :
        url = reverse('customer_order_update', args = ['89'])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class , CustomerOrderUpdateView)

    def test_ValidateUrl(self) :
        url = reverse('validate')
        print(resolve(url))
        self.assertEquals(resolve(url).func , validate)

    def test_AjaxCustomerUrl(self) :
        url = reverse('create_customers_ajax')
        print(resolve(url))
        self.assertEquals(resolve(url).func , create_customer_ajax)

    def test_LoginCustomerUrl(self) :
        url = reverse('login')
        print(resolve(url))
        self.assertEquals(resolve(url).func , login_user)

    def test_LogoutCustomerUrl(self) :
        url = reverse('logout')
        print(resolve(url))
        self.assertEquals(resolve(url).func , logout_user)




class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.store_url = reverse('store')

        user = User.objects.create(username= 'test', password = 'xaidi110786')
        self.product1 = Product.objects.create(
            name= 'shaban',
            price = 12,
        )
        self.detail_url = reverse('product_detail', args = [self.product1.pk])

    def testStoreView(self):

        response = self.client.get(self.store_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, os.path.join(settings.BASE_DIR, "templates/store/store.html"))

    def testProductDetailView(self):

        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, os.path.join(settings.BASE_DIR, "templates/store/product_detail.html"))



