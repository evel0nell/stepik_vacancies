"""stepik_vacancies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from vacancies.views import MainView, VacancyListView, VacancyView, \
    SpecialisationListView, CompanyView, CompanyListView, MySignupView, MyLoginView,\
    MyCompanyView, MyVacanciesView, MyVacancyEdit, MyVacancyCreateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
    path("vacancies/", VacancyListView.as_view()),
    path('vacancies/cat/<str:code>/', SpecialisationListView.as_view()),
    path('companies/<int:id>/', CompanyView.as_view()),
    path('vacancies/<int:id>/', VacancyView.as_view()),
    path('companies/', CompanyListView.as_view()),
    path('mycompany/', MyCompanyView.as_view()),
    path('mycompany/myvacancies', MyVacanciesView.as_view()),
    path('mycompany/myvacancies/edit/<int:id>', MyVacancyEdit.as_view() ),
    path('mycompany/myvacancies/create/',MyVacancyCreateView.as_view() ),
    path('login', MyLoginView.as_view()),
    path('signup', MySignupView.as_view()),
    path('logout', LogoutView.as_view())
]
handler404 = "vacancies.views.handler404"
handler500 = "vacancies.views.handler500"
