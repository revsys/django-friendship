from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'sample.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r"^friendship/", include("friendship.urls")),
    url(r"^admin/", admin.site.urls),
]
