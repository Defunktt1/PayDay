from django.conf.urls import url
from . import views


app_name = "register"

urlpatterns = [
    url(r'^register/$', views.SignUp.as_view(), name="register"),
    url(r'^login/$', views.SignIn.as_view(), name="login"),
    url(r'^logout/$', views.Logout.as_view(), name="logout"),
]
