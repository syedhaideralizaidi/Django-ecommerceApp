from django.urls import path
from . import views

urlpatterns = [
    path("", views.StoreView.as_view(), name="store"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("update_item/", views.UpdateItem.as_view(), name="update_item"),
]
