import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, Http404, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import CreateView
from stepik_vacancies.forms import MyCreationForm, ApplicationForm, EditMyCompanyForm, EditMyVacancyForm
from vacancies.models import Vacancy, Specialty, Company

specialities = Specialty.objects.all()
companies = Company.objects.all()
vacancies = Vacancy.objects.all()


class MainView(View):

    def get(self, request):
        # k - количество случайных элементов списка
        random_specialities = random.sample(set(specialities), k=4)


        return render(
            request, "vacancies/index.html", {"specialities": specialities,
                                              "companies": companies,
                                              "random_specialities": random_specialities}

        )


'''

ALL VACANCIES
'''


class VacancyListView(View):
    def get(self, request):
        return render(
            request, "vacancies/vacancies.html", {"vacancies": vacancies}
        )


class SpecialisationListView(View):
    def get(self, request, code):
        return render(
            request, "vacancies/vacancies_cat.html", {"vacancies": vacancies.filter(cat__code=code),
                                                      "title": Specialty.objects.get(code=code).title}
        )


class VacancyView(View):
    def get(self, request, id: int):
        return render(
            request, "vacancies/vacancy.html", {"vacancy": vacancies.get(id=id),
                                                'form': ApplicationForm}
        )


class CompanyView(View):
    def get(self, request, id: int):
        company = Vacancy.objects.filter(id=id).first()
        if not company:
            raise Http404
        return render(
            request, "vacancies/company.html", {"company": companies.get(id=id),
                                                "vacancies": vacancies.filter(company=id)}
        )


class CompanyListView(View):
    def get(self, request):
        return render(
            request, "vacancies/companies.html", {"companies": companies}
        )


class MyCompanyView(View):
    def get(self, request):
        form = EditMyCompanyForm

        return render(request, 'vacancies/company-edit.html', {'form': form})

    def post(self, request):
        form = EditMyCompanyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)

            user_company = Company.objects.create(name=data['name'], location=data['location'],
                                                  description=data['description'],
                                                  employee_count=data['employee_count'], owner=request.user
                                                  )

            user_company.save()

        return render(request, 'vacancies/company-edit.html', {'form': form})


class MyVacanciesView(View):
    def get(self, request):
        return render(request, "vacancies/company-myVacancies.html")


class MyVacancyEdit(View):
    def get(self, request):
        return render(request, "vacancies/company-vacancy-edit.html")


class MySignupView(View):
    def get(self, request):
        form = MyCreationForm()
        context = {
            'form': form
        }
        return render(request, 'vacancies/signup.html', context=context)

    def post(self, request):
        form = MyCreationForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            User.objects.create_user(
                username=user_data['username'],
                password=user_data['password'],

            )

        return render(request, 'vacancies/signup.html')

    success_url = 'login'
    template_name = 'vacancies/signup.html'


class MyLoginView(LoginView):
    template_name = 'vacancies/login.html'
    redirect_authenticated_user = True


'''
– Отправка заявки /vacancies/<vacancy_id>/send
– Моя компания /mycompany
– Мои вакансии /mycompany/vacancies
– Одна моя вакансия  /mycompany/vacancies/<vacancy_id>

'''


class SendVacancyView(View):
    def get(self, request):
        return render(request, 'vacancies/company-create.html')


def handler404(request, exception=None):
    return render(request, "404.html", status=404)


def handler500(request, exception=None):
    return render(request, "500.html", status=500)
