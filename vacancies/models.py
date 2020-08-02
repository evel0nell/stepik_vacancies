from django.db import models


class Specialty(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    picture = ...


class Company(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=50)
    logo = ...
    description = models.CharField(max_length=1000)
    employee_count = models.IntegerField()


class Vacancy(models.Model):
    title = models.CharField(max_length=50)
    cat = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = ...
    description = models.CharField(max_length=1000)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()
