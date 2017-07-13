from datetime import datetime
from django.views.generic import ListView, CreateView, FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from .models import Entry
from .forms import EntryForm, CountForm
from register.views import SignIn

class IndexView(ListView):
    http_method_names = ["get"]
    queryset = Entry.objects.order_by("-create_date")[:30]
    template_name = "payday/index.html"
    context_object_name = "last_third_entries"


class NewEntryView(CreateView):
    http_method_names = ["get", "post"]
    template_name = "payday/new.html"
    form_class = EntryForm
    success_url = "/"

    @method_decorator(login_required(login_url=reverse_lazy("register:login")))
    def dispatch(self, request, *args, **kwargs):
        return super(NewEntryView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.create_date = datetime.now()
        entry.save()
        return super(NewEntryView, self).form_valid(form)


class CountView(FormView):
    http_method_names = ["get", "post"]
    template_name = "payday/count.html"
    form_class = CountForm
    success_url = "/count"
    context_object_name = "result"

    def post(self, request, *args, **kwargs):
        form = request.POST

        date_interval = Entry.objects.filter(day__gte=form["from_date"]).filter(day__lte=form["to_date"])
        total_hours = 0
        for hours in date_interval:
            total_hours += hours.hours

        hour_rate = float(form["hour_rate"])
        exchange_rates = float(form["exchange_rates"])
        manager_rate = float(form["manager_rate"])
        company_rate = float(form["company_rate"])

        total_result = get_results(total_hours, hour_rate, exchange_rates, manager_rate, company_rate)
        content = super(CountView, self).get_context_data(**kwargs)
        content.update(total_result)

        return self.render_to_response(content, **kwargs)


def get_results(total_hours, hour_rate, exchange_rates, manager_rate, company_rate):
    total_money_in_usd = total_hours * hour_rate
    total_money_in_uan = total_money_in_usd * exchange_rates
    manager_result_in_usd = total_money_in_usd * (manager_rate / 100)
    company_result_in_usd = total_money_in_usd * (company_rate / 100)
    user_result_in_usd = total_money_in_usd - manager_result_in_usd - company_result_in_usd
    manager_result_in_uan = manager_result_in_usd * exchange_rates
    company_result_in_uan = company_result_in_usd * exchange_rates
    user_result_in_uan = user_result_in_usd * exchange_rates

    total_result = {
        "total_money_in_usd": total_money_in_usd,
        "total_money_in_uan": total_money_in_uan,
        "manager_result_in_usd": manager_result_in_usd,
        "manager_result_in_uan": manager_result_in_uan,
        "company_result_in_usd": company_result_in_usd,
        "company_result_in_uan": company_result_in_uan,
        "user_result_in_usd": user_result_in_usd,
        "user_result_in_uan": user_result_in_uan,
    }

    for key, result in total_result.items():
        if total_result[key].is_integer():
            total_result[key] = int(total_result[key])
        else:
            total_result[key] = float("{0:.2f}".format(result))

    return total_result
