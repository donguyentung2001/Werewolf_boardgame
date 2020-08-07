from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Character(models.Model): 
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.TextField(blank=True)
    ready=models.BooleanField(default=False)