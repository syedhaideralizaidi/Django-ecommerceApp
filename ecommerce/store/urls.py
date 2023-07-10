from django.urls import path
from . import views

urlpatterns = [
    path("", views.StoreView.as_view(), name="store"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("update_item/", views.UpdateItem.as_view(), name="update_item"),
    path("create_product/", views.ProductCreateView.as_view(), name="create_product"),
    path(
        "create_customer/", views.CustomerCreateView.as_view(), name="create_customer"
    ),
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
]
