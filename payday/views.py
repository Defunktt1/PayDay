from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods, require_GET
from datetime import datetime

from .models import Entry
from .forms import EntryForm, CountForm


@require_GET
def index(request):
    last_third_entries = Entry.objects.order_by("-create_date")[:30]
    return render(request, 'payday/index.html', {'last_third_entries': last_third_entries})


@require_GET
def settings(request):
    return HttpResponse('Site Settings')


@require_http_methods(['GET', 'POST'])
def add_new(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)

        if form.is_valid():
            data = form.save(commit=False)
            date = request.POST.get("day")
            date = date.replace("/", " ")
            data.day = datetime.strptime(date, '%d %m %Y')
            data.create_date = datetime.now()
            data.save()
            return HttpResponseRedirect('/')

    else:
        form = EntryForm()

    return render(request, 'payday/new.html', {'form': form})


@require_http_methods(['GET', 'POST'])
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
            user_name = request.POST.get('user_name')
            from_date = parse_time(from_date)
            to_date = parse_time(to_date)
            date_interval = Entry.objects.filter(day__gte=from_date).filter(day__lte=to_date)
            find_user = date_interval.filter(user_name__contains=user_name)

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
    date = date.replace("/", " ")
    return datetime.strptime(date, '%d %m %Y')
