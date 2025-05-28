from django.urls import path
from . import views
urlpatterns = [
    path('', views.Home.as_view()),
    path('create', views.UserListCreateAPIView.as_view()),
    path('change_password', views.UserChangePassAPIView.as_view()),
    path('new_project', views.ProductListCreateAPIView.as_view()),
]