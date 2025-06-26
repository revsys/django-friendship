from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # Examples:
    # url(r'^$', 'sample.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    path("friendship/", include("friendship.urls")),
    path("admin/", admin.site.urls),
]
