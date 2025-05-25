from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'user_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }