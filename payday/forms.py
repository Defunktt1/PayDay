from django import forms
from .models import Entry
from django.forms.widgets import SelectDateWidget


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = (
            'user_name',
            'hours',
            'work_description'
        )
        labels = {
            "hours": "Hours",
            "work_description": "Work description",
            "user_name": "Your name",
        }


class CountForm(forms.Form):
    hour_rate = forms.FloatField(label="Зарплата за час:", min_value=0.0)
    company_rate = forms.FloatField(label="Сколько забирает фирма (в процентах):", min_value=0.0)
    manager_rate = forms.FloatField(label="Сколько забирает менеджер (в процентах):", min_value=0.0)
    exchange_rates = forms.FloatField(label="Курс гривны:", min_value=0.0)
