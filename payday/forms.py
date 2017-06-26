from django import forms
from .models import Entry
from django.forms.widgets import SelectDateWidget


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('hours', 'work_description')


class CountForm(forms.Form):
    from_date = forms.DateField(label="От:", widget=SelectDateWidget)
    to_date = forms.DateField(label="До:", widget=SelectDateWidget)
    hour_rate = forms.FloatField(label="Зарплата за час:", min_value=0.0)
    company_rate = forms.FloatField(label="Сколько забирает фирма:", min_value=0.0)
