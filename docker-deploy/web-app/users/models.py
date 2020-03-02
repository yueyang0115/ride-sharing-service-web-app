from django.db import models
from django.contrib.auth.models import User

TYPE_CHOICES = (
    ("SUV", "SUV"),
    ("COMPACT", "COMPACT"),
    ("SEDAN", "SEDAN"),
    ("COUPE", "COUPE"),
)

class Driver_info(models.Model):   
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    license_number = models.CharField(max_length = 10, default = '',blank=True)
    max_number = models.PositiveIntegerField(default = 0)
    vehicle_type = models.CharField(max_length = 20, choices = TYPE_CHOICES, default = 'SUV')
    special_info = models.TextField(blank = True, default = '')

    def __str__(self):
        return f'{self.user.username} Driver_info'
