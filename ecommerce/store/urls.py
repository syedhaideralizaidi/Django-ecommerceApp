from django.urls import path
from . import views

urlpatterns = [
    path("", views.StoreView.as_view(), name="store"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("update_item/", views.UpdateItem.as_view(), name="update_item"),
    path(
        "create_customer/", views.CustomerCreateView.as_view(), name="create_customer"
    ),
    path("create_product/", views.ProductCreateView.as_view(), name="create_product"),
    path("product_list/", views.ProductListView.as_view(), name="product_list"),
    path(
        "product/<str:name>/update/",
        views.ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "customer/<str:name>/delete/",
        views.CustomerDeleteView.as_view(),
        name="customer_delete",
    ),
    path("template/", views.TemplateHomeView.as_view(), name="template_view"),
    path("order_archive/", views.OrderArchiveView.as_view(), name="order_archive"),
    path(
        "product_detail/<int:pk>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "orderitem_create/", views.OrderItemCreateView.as_view(), name="product_detail"
    ),
    path(
        "dayarchive/<int:year>/",
        views.OrderDayArchiveView.as_view(),
        name="order_archive_day",
    ),
    path(
        "customer/<str:name>/update/",
        views.CustomerUpdateView.as_view(),
        name="customer_update",
    ),
    path("createcustomerFBW/", views.customer_create_view, name="customercreate_FBW"),
    path(
        "deletecustomerFBW/<str:name>/",
        views.customer_delete_view,
        name="deletecreate_FBW",
    ),
    path(
        "updatecustomerFBW/<str:name>/",
        views.customer_update_view,
        name="customerupdate_FBW",
    ),
    path("customer/<str:name>", views.customer_view, name="customer"),
    path("customer/", views.customer_view, name="customer"),
]
