from django.db import models

from django.contrib.auth.models import User




class Specialty(models.Model):




    code = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    picture = ...

    def __str__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=50)
    logo = ...
    description = models.CharField(max_length=1000)
    employee_count = models.IntegerField()
    def __str__(self):
        return self.name

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company', null=True)



class Vacancy(models.Model):
    title = models.CharField(max_length=50)
    cat = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = ...
    description = models.CharField(max_length=1000)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()
    def __str__(self):
        return self.title



class Application(models.Model):
    written_username = models.CharField(max_length=50)
    written_phone = models.IntegerField()
    written_cover_letter = models.CharField(max_length=1000)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")
#   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

