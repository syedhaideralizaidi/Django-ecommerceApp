from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


admin.site.site_header = "Ecommerce Website"
admin.site.site_title = "Ecommerce Store"
admin.site.index_title = "Welcome to this Ecommerce Portal"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("store.urls")),
    path("", include("django.contrib.auth.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
