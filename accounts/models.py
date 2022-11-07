from django.db import models
import datetime
from django.utils import timezone
import time as t


class Account(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=100)
    isAuthorized = models.BooleanField(default=False)
    creation_time = models.TimeField(default= datetime.datetime.now())
#     auth_token = models.CharField(max_length=100, default='')

          

class authTokenModel(models.Model):
        auth_token = models.CharField(max_length=100)
        user = models.OneToOneField(Account, on_delete= models.CASCADE)
        publishing_time = models.TimeField(default=datetime.datetime.now())


# class Event(models.Model):
#     name = models.CharField(
#         max_length=100,
#         )
#     publishing_time = models.TimeField(
#     default=datetime.datetime.now(),
#     blank=True,
#     )


# import datetime
# from celery.schedules import crontab
# from celery.task import periodic_task
# from django.utils import timezone

# @periodic_task(run_every=crontab(minute='*/1'))
# def delete_old_orders():
#         print("hii")
#         d = timezone.now() - datetime.timedelta(minutes=1)
#         authTokenModel.objects.filter(publishing_time__lte=d).delete()
#         authTokenModel.delete()
