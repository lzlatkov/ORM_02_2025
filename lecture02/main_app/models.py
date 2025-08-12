from datetime import date

from django.db import models

# Create your models here.


class Department(models.Model):

    class Cities(models.TextChoices):
        Sofia = 'Sofia', 'Sofia'
        Plovdiv = 'Plovdiv', 'Plovdiv'
        Burgas = 'Burgas', 'Burgas'
        Varna = 'Varna', 'Varna'

    code = models.CharField(
        max_length=4,
        primary_key=True,
        unique=True
    )
    name = models.CharField(max_length=50, unique=True)
    employees_count = models.IntegerField(default=1, verbose_name='Employee Count')
    location = models.CharField(max_length=20, null=True, blank=True, choices=Cities.choices)
    last_edited_on = models.DateTimeField(auto_now=True, editable=False)


class Employee(models.Model):
    name = models.CharField(max_length=30)
    email_address = models.EmailField()
    photo = models.URLField()
    birth_date = models.DateField()
    works_full_time = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    budget = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
    duration_in_days = models.IntegerField(blank=True, null=True, verbose_name='Duration in Days')
    estimated_hours = models.FloatField(blank=True, null=True, verbose_name='Estimated Hours')
    start_date = models.DateField(default=date.today(), blank=True, null=True, verbose_name='Start Date')
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_edited_on = models.DateTimeField(auto_now=True, editable=False)