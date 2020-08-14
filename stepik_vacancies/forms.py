from django import forms
from django.forms import ModelForm
from vacancies.models import Company, Vacancy


class MyCreationForm(forms.Form):
    username = forms.CharField(max_length=100)
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    password = forms.CharField(min_length=8, max_length=100)


class MyAutorisationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

class ApplicationForm(forms.Form):
    name = forms.CharField(max_length=100)
    telefon = forms.IntegerField()
    cover_letter = forms.CharField(max_length=1000)

class EditMyCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location', 'description', 'employee_count']
class EditMyVacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'cat', 'company',
                  'description', 'salary_min',
                  'salary_max', 'published_at']


