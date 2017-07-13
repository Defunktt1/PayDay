from .forms import RegisterForm, LoginForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, FormView, RedirectView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


class SignUp(SuccessMessageMixin, CreateView):
    template_name = "register/register.html"
    form_class = RegisterForm
    success_url = "/"
    success_message = "Регистрация прошла успешно"

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(SignUp, self).form_valid(form)


class SignIn(FormView):
    template_name = "register/login.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return super(SignIn, self).form_valid(form)


class Logout(RedirectView):
    url = "/"

    @method_decorator(login_required(login_url=reverse_lazy("register:login")))
    def dispatch(self, request, *args, **kwargs):
        return super(Logout, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Logout, self).get(request, *args, **kwargs)
