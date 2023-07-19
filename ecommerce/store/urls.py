from django.urls import path

from . import views
from .formsetViews import *

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("", views.StoreView.as_view(), name="store"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("update_item/", views.UpdateItem.as_view(), name="update_item"),
    path("product_/", views.ProductCreateView.as_view(), name="create_product"),
    path("product_list/", views.ProductListView.as_view(), name="product_list"),
    #path("product_list/", views.product_list, name="product_list"),
    path(
        "product_/<str:name>/",
        views.ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "product_l/<int:pk>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "product_/<str:name>/delete/",
        views.ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path("template/", views.TemplateHomeView.as_view(), name="template_view"),
    path("order_archive/", views.OrderArchiveView.as_view(), name="order_archive"),
    path(
        "orderitem_create/", views.OrderItemCreateView.as_view(), name="product_detail"
    ),
    path(
        "day_archive/<int:year>/",
        views.OrderDayArchiveView.as_view(),
        name="order_archive_day",
    ),
    path("customer_", views.CustomerCreateView.as_view(), name="customer"),
    path(
        "customer_/<str:name>",
        views.CustomerUpdateView.as_view(),
        name="customer_update",
    ),
    # path(
    #     "customer_/<str:name>/delete",
    #     views.CustomerDeleteView.as_view(),
    #     name="customer_delete",
    # ),
    path(
        "customer_/<int:pk>/delete",
        views.CustomerDeleteView.as_view(),
        name="customer_delete",
    ),
    path("checkc_/create", views.CheckView.as_view(), name="create_customer"),
    path(
        "checkc_",
        views.CheckView.as_view(),
        name="customer_list",
    ),
    path(
        "checkc_/<int:pk>/update" ,
        views.CheckView.as_view(template_name='templates/store/customer_form.html') ,
        name = "update_customer" ,
    ) ,
    path(
        "checkc_/<int:pk>" ,
        views.CheckView.as_view(template_name='templates/store/customer_detail.html') ,
        name = "customer_detail" ,
    ) ,
    path(
        "checkc_/<int:pk>/delete" ,
        views.CheckView.as_view(template_name='templates/store/customer_confirm_delete.html') ,
        name = "customer_delete1" ,
    ),
    path("order", views.OrderCreateView.as_view(), name = 'order_create'),
    path("order/<int:pk>/update", views.OrderUpdateView.as_view(template_name= 'templates/store/order_update.html'), name = 'update_order'),
    path("order/<int:pk>/delete", views.OrderDeleteView.as_view(template_name= 'templates/store/order_delete.html'), name = 'delete_order'),







    path("fvhome",HomeView.as_view(), name="fvhome"),
    path("fvhome/orders", CustomersViewList.as_view(), name = 'fvhome_customerlist'),
    path("fvhome/add", CustomersAddView.as_view(), name = 'add_customer'),
    path("fvhome/<int:pk>/", CustomerDetailView.as_view(), name = 'detail_customer'),
    path("fvhome/<int:pk>/orders/edit/", CustomerOrderUpdateView.as_view(), name = 'customer_order_update'),


    path("createcustomersajax", create_customer_ajax, name='create_customers_ajax'),
    path('validate',validate,name="validate"),
    path('get_customers', get_customers, name='get_customers'),




]
