from django.db import models

# Create your models here.

class GroupChat(models.Model): 
    name=models.TextField() 
    users_list=models.TextField()
    roles=models.TextField(default="werewolf,villager,villager,villager")

    def __str__(self): 
        return self.name 

class Choice(models.Model): 
    option_one=models.TextField(default="")
    option_two=models.TextField(default="")
    option_three=models.TextField(default="")
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)
    option_three_count = models.IntegerField(default=0)
