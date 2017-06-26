from django.conf.urls import url
from . import views

app_name = "payday"

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^settings/$', views.settings, name="settings"),
    url(r'^new/$', views.add_new, name="new"),
    url(r'^count/$', views.count, name="count"),
]
