import random
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, Http404, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import CreateView
from stepik_vacancies.forms import MyCreationForm, ApplicationForm, \
    EditMyCompanyForm, EditMyVacancyForm, MyAutorisationForm
from vacancies.models import Vacancy, Specialty, Company




class MainView(View):

    def get(self, request):
        specialities= Specialty.objects.all()
        companies = Company.objects.all()
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
        vacancies = Vacancy.objects.all()
        return render(
            request, "vacancies/vacancies.html", {"vacancies": vacancies}
        )


class SpecialisationListView(View):
    def get(self, request, code):
        vacancies = Vacancy.objects.all()
        return render(
            request, "vacancies/vacancies_cat.html", {"vacancies": vacancies.filter(cat__code=code),
                                                      "title": Specialty.objects.get(code=code).title}
        )


class VacancyView(View):


    def get(self, request, id: int):
        vacancies = Vacancy.objects.all()
        return render(
            request, "vacancies/vacancy.html", {"vacancy": vacancies.get(id=id),
                                                'form': ApplicationForm()}
        )

    def post(self, request, id: int):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

        return render(request, "vacancies/index.html", {'form': form})


class CompanyView(View):
    def get(self, request, id: int):
        vacancies = Vacancy.objects.all()
        companies = Company.objects.all()
        company = companies.get(id=id)
        return render(
            request, "vacancies/company.html", {"company": company,
                                                "vacancies": vacancies.filter(company=company)}
        )


class CompanyListView(View):
    def get(self, request):
        companies = Company.objects.all()
        return render(
            request, "vacancies/companies.html", {"companies": companies}
        )


class MyCompanyView(View):
    def get(self, request):

        if not Company.objects.filter(owner=request.user).exists():
            return render(request, 'vacancies/company-create.html')
        else:
            form = EditMyCompanyForm
            return render(request, 'vacancies/company-edit.html', {'form': form})

    def post(self, request):
        form = EditMyCompanyForm(request.POST)
        user_company = Company.objects.get(owner=request.user)
        if form.is_valid():
            data = form.cleaned_data
            user_company.name=data['name'],
            user_company.location=data['location'],
            user_company.description=data['description'],
            user_company.data['employee_count']

            user_company.save()

        return render(request, 'vacancies/company-edit.html', {'form': form})

class MyCompanyCreate(View):
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
        user = request.user
        company = Company.objects.get(owner=user)
        vacancies = Vacancy.objects.filter(company=company)
        if company.vacancies.exists():
            return render(request, "vacancies/company-myVacancies-List.html", {'vacancies': vacancies})

        else:
            return render(request, "vacancies/company-myVacancies-None.html")


class MyVacancyEdit(View):

    def get(self, request, id: int):
        vacancies=Vacancy.objects.all()
        form = EditMyVacancyForm()
        return render(request, "vacancies/company-vacancy-edit.html", {'vacancy': vacancies.get(id=id),
                                                                       'form': form})

    def post(self, request, id: int):
        form = EditMyVacancyForm(request.POST)
        user = request.user

        user_vacancy = Vacancy.objects.get(id=id)
        if form.is_valid():
            data = form.cleaned_data

            user_vacancy.title=data['title']

            user_vacancy.description=data['description'],
            user_vacancy.salary_max=data['salary_max']
            user_vacancy.salary_min=data['salary_min']



            user_vacancy.save()
        else:
            print('data is not valid')


        return render(request, "vacancies/company-vacancy-edit.html", {'form': form})


class MyVacancyCreateView(View):

    def get(self, request):
        form = EditMyVacancyForm()

        list = Specialty.objects.all()

        return render(request, "vacancies/company-vacancy-edit.html", {'form': form, 'list': list})

    def post(self, request):
        form = EditMyVacancyForm(request.POST)
        user = request.user

        if form.is_valid():
            data = form.cleaned_data

            user_vacancy = Vacancy.objects.create(title=data['title'], cat=data['cat'],
                                                  description=data['description'], salary_max=data['salary_max'],
                                                  salary_min=data['salary_min'], published_at=datetime.now(),
                                                  company=Company.objects.get(owner=request.user)

                                                  )

            user_vacancy.save()
        else:
            print('data is not valid')

        return render(request, "vacancies/company-vacancy-edit.html", {'form': form})


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


class MyLoginView(View):
    def get(self, request):
        form = MyAutorisationForm()
        return render(request, 'vacancies/login.html', {'form': form})

    def post(self, request):
        form = MyAutorisationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            username = data['username']
            password = data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                response = redirect('/')
                return response


            else:
                raise Http404
        return render(request, 'vacancies/login.html', {'form': form})


class SendVacancyView(View):
    def get(self, request):
        return render(request, 'vacancies/company-create.html')


def handler404(request, exception=None):
    return render(request, "404.html", status=404)


def handler500(request, exception=None):
    return render(request, "500.html", status=500)
