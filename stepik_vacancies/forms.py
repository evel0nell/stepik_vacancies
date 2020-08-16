from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, TextInput, NumberInput, ModelChoiceField
from vacancies.models import Company, Vacancy, Specialty


class MyCreationForm(forms.Form):
    username = forms.CharField(max_length=100)
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    password = forms.CharField(min_length=8, max_length=100)


class MyAutorisationForm(forms.Form):
    username = forms.CharField(max_length=100, label='Login', widget=forms.TextInput(
        attrs={
            'class': "form-control", 'type': "text",
            'id': "inputLogin"

        }
    ))
    password = forms.CharField(max_length=100, label='Password', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'inputPassword',
               'type': 'password'}))


class ApplicationForm(forms.Form):
    name = forms.CharField(max_length=100, label='Вас зовут', widget=forms.TextInput(
        attrs={
            'class': "form-control",
            "type": 'text'}
    ))
    telefon = forms.IntegerField(label="Ваш телефон", widget=forms.NumberInput(
        attrs={
            'class': "form-control", "type": 'integer'
        }
    ))
    cover_letter = forms.CharField(max_length=1000, label="Сопроводительное письмо", widget=forms.Textarea(
        attrs={'class': "form-control", 'type': 'text'}
    ))


class EditMyCompanyForm(ModelForm):
    class Meta:
        model = Company
        TextAttrib = {'class': 'form-control', 'type': 'text'}
        fields = ['name', 'location', 'description', 'employee_count']
        widgets = {
            'name': TextInput(attrs=TextAttrib),
            'location': TextInput(attrs=TextAttrib),
            'description': Textarea(attrs=TextAttrib),
            'employee_count': NumberInput(attrs={'class': 'form-control'})
        }



'''<input class="form-control" type="text" value="Staffing Smarter" id="companyName">'''


class EditMyVacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title','cat',
                  'description', 'salary_min',
                  'salary_max']
        labels = {'title': "Название вакансии", 'cat': "Категория",
                  'description': "Описание", 'salary_min': "до",
                  'salary_max': "Зарплата от"}
        CHOICES = (('Option1', Specialty.objects.get(id=2)))
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'value': 'Your company name',
                'id': "vacancyTitle"
            }),

            'description': Textarea(attrs={'class': 'form-control', 'rows': 13}),

            'salary_max': TextInput(attrs={'class': 'form-control',
                                             'type': 'text',
                                             'value': '90000',
                                             'id': 'vacancySalaryMax'}),
            'salary_min': TextInput(attrs={'class': 'form-control',
                                             'type': 'text',
                                             'value': '90000',
                                             'id': 'vacancySalaryMin'})

        }
