from django.conf.urls import url
from . import views

app_name = "payday"

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^new/$', views.NewEntryView.as_view(), name="new"),
    url(r'^count/$', views.CountView.as_view(), name="count"),
]
