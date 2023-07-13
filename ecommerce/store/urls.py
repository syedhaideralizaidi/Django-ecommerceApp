from django.urls import path, include
from . import views
from django.contrib.auth import admin


urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("", views.StoreView.as_view(), name="store"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("update_item/", views.UpdateItem.as_view(), name="update_item"),
    path("product_/", views.ProductCreateView.as_view(), name="create_product"),
    path("product_list/", views.ProductListView.as_view(), name="product_list"),
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
    path(
        "customer_/<str:name>/delete",
        views.CustomerDeleteView.as_view(),
        name="customer_delete",
    ),
    path("checkc_", views.CheckView.as_view(), name="checkcustomer"),
    path(
        "checkc_/<int:id>/update",
        views.CheckView.as_view(),
        name="checkcustomer_update",
    ),
    path(
        "checkc_/<str:name>/delete",
        views.CheckView.as_view(),
        name="checkcustomer_update",
    ),
]
