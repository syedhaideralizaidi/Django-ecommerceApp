from django.urls import path , re_path

from . import views

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
        name = "customer_delete" ,
    ) ,
    # path(r'admin/store/order/<int:object_id>/change' , admin.site.admin_view(OrderAdmin.change_view)) ,
    re_path(r'^admin/store/order/(?P<object_id>\d+)/change/$', views.store_order_change, name='store_order_change')


]
