from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Custom Admin Site Title and Headers in Persian
admin.site.site_header = "پنل مدیریت پلتفرم موسیقی بهاور"
admin.site.site_title = "بهاور موزیک | مدیریت استودیو و آکادمی"
admin.site.index_title = "میز کار مدیریت بهاور موزیک"

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # REST APIs
    path('api/accounts/', include('accounts.urls', namespace='accounts')),
    path('api/shop/', include('shop.urls', namespace='shop')),
    path('api/booking/', include('booking.urls', namespace='booking')),
    path('api/blog/', include('blog.urls', namespace='blog')),
    path('api/repertoire/', include('repertoire.urls', namespace='repertoire')),
    path('api/core/', include('core.urls', namespace='core')),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
