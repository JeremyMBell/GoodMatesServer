from django.conf.urls import include, url
from django.contrib import admin
from GoodMatesServer import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'src.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^create_user/$', views.create_user),
]
