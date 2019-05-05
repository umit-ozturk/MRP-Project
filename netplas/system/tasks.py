from __future__ import absolute_import, unicode_literals
from celery import task
from profile.models import UserProfile
from system.models import Budget
from decimal import Decimal


@task()
def task_pay_salaries():
    total_salary = Decimal(0)
    users = UserProfile.objects.filter()
    for user in users:
        total_salary += user.salary
    budget = Budget.objects.filter().first()
    Budget.objects.create(salaries=total_salary, total=budget.total)
