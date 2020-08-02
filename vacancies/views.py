import random

from django.shortcuts import render, Http404
from django.views import View

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
            request, "vacancies/vacancy.html", {"vacancy": vacancies.get(id=id)}
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
def handler404(request, exception=None):
    return render(request, "404.html", status=404)


def handler500(request, exception=None):
    return render(request, "500.html", status=500)
