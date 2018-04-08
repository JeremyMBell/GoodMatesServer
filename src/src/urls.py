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
    url(r'^book_shower/$', views.book_shower),
    url(r'^note_payment/$', views.note_payment),
    url(r'^note_guests/$', views.note_guests),
    url(r'^note_chore/$', views.note_chore),
    url(r'^note_plan/$', views.note_plan),
    url(r'^get_user/$', views.get_user),
    url(r'^get_group/$', views.get_group),
    url(r'^get_laundry/$', views.get_laundry),
    url(r'^get_shower/$', views.get_shower),
    url(r'^get_payment/$', views.get_payment),
    url(r'^get_guests/$', views.get_guests),
    url(r'^get_chore/$', views.get_chore),
    url(r'^get_plan/$', views.get_plan)

]
