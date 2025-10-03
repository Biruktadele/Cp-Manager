from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    codeforces_handle = models.CharField(max_length=100, unique=True ,blank=True, null=True)
    leetcode_handle = models.CharField(max_length=100, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = CloudinaryField('avatars', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    rating = models.IntegerField(default=1500)
    div = models.CharField(max_length=10, choices=[('Div. 1', 'Div. 1'), ('Div. 2', 'Div. 2'), ('Community', 'Community')], default='Div. 2')
    
    def __str__(self):
        return self.username
class Team(models.Model):
    team_name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User, related_name='teams')
    team_rating = models.IntegerField(default=1500)

# Create your models here.
