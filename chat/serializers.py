from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import Character
# Create your views here.

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['user','role']

class UserSerializer(serializers.ModelSerializer):
    character=CharacterSerializer(read_only=True)
    class Meta:
        model = User
        fields = '__all__'

    