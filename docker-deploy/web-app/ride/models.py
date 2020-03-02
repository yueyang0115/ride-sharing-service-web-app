from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

TYPE_CHOICES = (
    ("SUV", "SUV"),
    ("COMPACT", "COMPACT"),
    ("SEDAN", "SEDAN"),
    ("COUPE", "COUPE"),
    ("--", "--"),
)


class Rideowner(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    addr = models.CharField(max_length=100)
    arrive_date = models.DateTimeField(help_text='Format: 2020-01-01 12:00')
    passenger_num = models.PositiveIntegerField(default=1)
    whether_share = models.BooleanField()
    max_share_num = models.PositiveIntegerField(help_text='If you do not want to share please choose 0', default=0)
    required_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='--')
    required_special = models.CharField(max_length=400, blank=True)
    status = models.CharField(default='open', max_length=20)
    share_name = models.CharField(default='', max_length=50, blank=True)
    share_num = models.PositiveIntegerField(default=0)
    driver_name = models.CharField(default='', max_length=50, blank=True)
    driver_license = models.CharField(default='', max_length=50, blank=True)


    def __str__(self):
        return self.addr
    #When submit, the webpage will go to the certain place
    def get_absolute_url(self):
        return reverse('rideowner-list')



class Ridesharer(models.Model):
    sharer = models.ForeignKey(User, on_delete=models.CASCADE)
    addr = models.CharField(max_length=100)
    earliest_arrive_date = models.DateTimeField(help_text='Format: 2020-01-01 12:00')
    latest_arrive_date = models.DateTimeField(help_text='Format: 2020-01-01 13:00')
    passenger_num = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.addr
    #When submit, the webpage will go to the certain place
    def get_absolute_url(self):
        return reverse('ridesharer-list')



