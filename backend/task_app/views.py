from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from .models import *
from .serializers import *
from .permissions import *

User = get_user_model()
class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(request, *args, **kwargs):
        return Response({"message" : "Hello World"})
    
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = serializer.validated_data.get('password')
        serializer.save(password=make_password(password))
        return Response({"message" : "Successfully Created!"})


class UserChangePassAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def patch(self, request, *args, **kwargs):
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        if new_password != confirm_password:
            return Response({"error" : "Passwords do not match"})
        
        user = request.user
        user.set_password(new_password)
        user.save()
        
        return Response({"message" : "Password changed successfully"})

class ProductListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsProjectOwner]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

class TaskListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsProjectLead]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    def perform_create(self, serializer):
        serializer.save()

class PurchaseListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsProjectOwner]
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    def perform_create(self, serializer):
        supplier_name = self.request.data.get('supplier')
        supplier_instance = Supplier.objects.get(supplier_org=supplier_name)
        serializer.save(raised_by=self.request.user, supplier=supplier_instance)
