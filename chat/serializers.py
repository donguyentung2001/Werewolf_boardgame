from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import Character
from .models import Choice
# Create your views here.
 
class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
       model = Character
       fields = ['user','role','death']
 
class UserSerializer(serializers.ModelSerializer):
    character=CharacterSerializer(read_only=True)
    class Meta:
       model = User
       fields = '__all__'

    def create(self, validated_data):
        characters_data = validated_data.pop('characters')
        user = User.objects.create(**validated_data)
        for character_data in characters_data:
            Character.objects.create(user=user, **user_data)
        return user

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
       model = Choice
       fields = '__all__'