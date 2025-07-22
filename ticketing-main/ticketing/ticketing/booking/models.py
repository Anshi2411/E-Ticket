from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import date

def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True)
    gender = models.CharField(
    max_length=10,
    blank=True,
    null=True,  # add this!
    choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    )
    occupation = models.CharField(
    max_length=50,
    blank=True,
    null=True,  # add this!
    choices=[('Student', 'Student'), ('Working Professional', 'Working Professional')]
    )

    def __str__(self):
        return self.user.username

class Recharge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ₹{self.amount}"

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_station = models.CharField(max_length=100)
    to_station = models.CharField(max_length=100)
    fare = models.DecimalField(max_digits=6, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user.username} - {self.from_station} to {self.to_station} at {self.timestamp}"
