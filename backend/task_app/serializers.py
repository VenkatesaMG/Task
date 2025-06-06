from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'user_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_name', 'description', 'start_date', 'end_date', 'budget']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['project_id', 'task_name', 'description', 'priority', 'status', 'deadline']

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['project_id', 'products', 'status', 'date']