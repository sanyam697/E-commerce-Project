from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'product/',include('products.urls')),
    path('',include('accounts.urls')),
    path('search/',include('search.urls')),
    path('carts/',include('carts.urls')),
    path('address/',include('addresses.urls')),
    path('accounts/', include('accounts.passwords.urls')),
    path('orders/',include('orders.urls')),
    path('invoice/',include('invoices.urls')),

]

if settings.DEBUG:
    urlpatterns= urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns= urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)