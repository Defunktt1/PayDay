from django.conf.urls import url
from . import views


app_name = "register"

urlpatterns = [
    url(r'^register/$', views.register, name="register"),
    # url(r'^logout/$', views.logout, name="logout"),
]
