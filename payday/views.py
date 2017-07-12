from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, CreateView, FormView
from django.contrib import messages

from .models import Entry
from .forms import EntryForm, CountForm


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

    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.create_date = datetime.now()
        return super(NewEntryView, self).form_valid(form)


class CountView(FormView):
    http_method_names = ["get", "post"]
    template_name = "payday/count.html"
    form_class = CountForm
    success_url = "/count"

    def form_valid(self, form):
        data = form.cleaned_data

        date_interval = Entry.objects.filter(day__gte=data["from_date"]).filter(day__lte=data["to_date"])
        total_hours = 0
        for hours in date_interval:
            total_hours += hours.hours

        total_money_in_usd = total_hours * data["hour_rate"]
        total_money_in_uan = total_money_in_usd * data["exchange_rates"]
        manager_result_in_usd = total_money_in_usd * (data["manager_rate"] / 100)
        company_result_in_usd = total_money_in_usd * (data["company_rate"] / 100)
        user_result_in_usd = total_money_in_usd - manager_result_in_usd - company_result_in_usd
        manager_result_in_uan = manager_result_in_usd * data["exchange_rates"]
        company_result_in_uan = company_result_in_usd * data["exchange_rates"]
        user_result_in_uan = user_result_in_usd * data["exchange_rates"]

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
            total_result[key] = float("{0:2f}".format(result))

        return super(CountView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CountView, self).get_context_data(**kwargs)
        print(context)
        context["total_money_in_usd"] = 50
        return context


def count(request):
    if request.method == 'POST':
        form = CountForm(request.POST)

        if form.is_valid():
            request_data = form.cleaned_data

            # basic response
            response = {
                "form": form,
            }

            # get date interval between two dates
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            from_date = parse_time(from_date)
            to_date = parse_time(to_date)
            date_interval = Entry.objects.filter(day__gte=from_date).filter(day__lte=to_date)

            # check if data is valid
            date_is_valid = from_date <= to_date

            if not date_is_valid:
                response["date_error"] = "Первая дата должна быть меньше второй"

            # count hours
            total_hours = 0
            check_hours = date_interval.exists()
            if not check_hours:
                response["hours_error"] = "Вы не работали в эти дни"

            if date_is_valid and check_hours:
                for hours in date_interval:
                    total_hours += hours.hours

                # set data from request to variables
                hour_rate = request_data['hour_rate']
                exchange_rates = request_data['exchange_rates']
                manager_rate = request_data['manager_rate']
                company_rate = request_data['company_rate']

                # count operations
                total_money_in_usd = total_hours * hour_rate
                total_money_in_uan = total_money_in_usd * exchange_rates
                manager_result_in_usd = total_money_in_usd * (manager_rate / 100)
                company_result_in_usd = total_money_in_usd * (company_rate / 100)
                user_result_in_usd = total_money_in_usd - manager_result_in_usd - company_result_in_usd
                manager_result_in_uan = manager_result_in_usd * exchange_rates
                company_result_in_uan = company_result_in_usd * exchange_rates
                user_result_in_uan = user_result_in_usd * exchange_rates

                # set all data to dict
                total_result = {
                    "total_money_in_usd": total_money_in_usd,
                    "total_money_in_uan": total_money_in_uan,
                    "manager_result_in_usd": manager_result_in_usd,
                    "manager_result_in_uan": manager_result_in_uan,
                    "company_result_in_usd": company_result_in_usd,
                    "company_result_in_uan": company_result_in_uan,
                    "user_result_in_usd": user_result_in_usd,
                    "user_result_in_uan": user_result_in_uan,
                    "response_check": True,
                }

                # limiting to two demical points
                for key, result in total_result.items():
                    total_result[key] = float("{0:2f}".format(result))

                # update response dict
                response.update(total_result)

            return render(request, 'payday/count.html', context=response)

    else:
        form = CountForm()

    return render(request, 'payday/count.html', {'form': form})


def parse_time(date):
    date = date.replace("-", " ")
    return datetime.strptime(date, '%d %m %Y')
