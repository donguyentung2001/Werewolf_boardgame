from django.contrib.auth.models import User
from rest_framework import serializers
# Create your views here.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'