from django import forms
from .models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = (
            'user_name',
            'hours',
            'work_description'
        )
        labels = {
            "hours": "Часы",
            "work_description": "Описание работы",
            "user_name": "Ваше имя",
        }


class CountForm(forms.Form):
    hour_rate = forms.FloatField(label="Зарплата за час:", min_value=0.0)
    company_rate = forms.FloatField(label="Сколько забирает фирма (в процентах):", min_value=0.0)
    manager_rate = forms.FloatField(label="Сколько забирает менеджер (в процентах):", min_value=0.0)
    exchange_rates = forms.FloatField(label="Курс гривны:", min_value=0.0)
    user_name = forms.CharField(label="Ваше имя:", min_length=1, max_length=50)
