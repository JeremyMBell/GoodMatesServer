from django.conf.urls import include, url
from django.contrib import admin
from GoodMatesServer import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'src.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^create_user/$', views.create_user),
    url(r'^create_group/$', views.create_group),
    url(r'^join_group/$', views.join_group),
    url(r'^book_laundry/$', views.book_laundry),
    url(r'^book_shower/$', views.book_shower)
]
