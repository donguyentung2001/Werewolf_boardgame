from django.db import models

# Create your models here.

class GroupChat(models.Model): 
    name=models.TextField() 
    users_list=models.TextField()
    roles=models.TextField(default="werewolf,villager,villager,villager")

    def __str__(self): 
        return self.name 