from django import forms
from .models import Entry


class EntryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial["hours"] = 8
        kwargs['initial'] = initial
        super(EntryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Entry
        fields = (
            "day",
            "hours",
            "work_description"
        )
        labels = {
            "day": "День",
            "hours": "Отработанное время",
            "work_description": "Описание работы",
        }
        initials = {
            "hours": 8,
        }


class CountForm(forms.Form):
    from_date = forms.DateField()
    to_date = forms.DateField()
    hour_rate = forms.FloatField(label="Зарплата за час (в долларах):", min_value=0.0, initial=5)
    company_rate = forms.FloatField(label="Сколько забирает фирма (в процентах):", min_value=0.0, initial=37)
    manager_rate = forms.FloatField(label="Сколько забирает менеджер (в процентах):", min_value=0.0, initial=8)
    exchange_rates = forms.FloatField(label="Курс гривны:", min_value=0.0, initial=25)

    def clean_to_date(self):
        from_date = self.cleaned_data.get("from_date")
        to_date = self.cleaned_data.get("to_date")

        if from_date > to_date:
            raise forms.ValidationError("Первая дата должна быть меньше второй")

        if not Entry.objects.filter(day__gte=from_date).filter(day__lte=to_date).exists():
            raise forms.ValidationError("Вы не работали в эти дни")

        return to_date
