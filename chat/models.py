from django.db import models

# Create your models here.

class GroupChat(models.Model): 
    name=models.TextField() 
    users_list=models.TextField()

    def __str__(self): 
        return self.name 