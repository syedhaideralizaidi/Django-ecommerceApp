from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

admin.site.site_header = "Ecommerce Website"
admin.site.site_title = "Ecommerce Store"
admin.site.index_title = "Welcome to this Ecommerce Portal"

urlpatterns = [
    path("", include("store.urls")),
    path("", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path(r'^i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += i18n_patterns (
    path("", include("store.urls")),
)

# urlpatterns += (r'^i18n/', include('django.conf.urls.i18n'))
