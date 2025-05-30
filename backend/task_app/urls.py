from django.urls import path
from . import views
urlpatterns = [
    path('', views.Home.as_view()),
    path('create_user', views.UserListCreateAPIView.as_view()),
    path('change_password', views.UserChangePassAPIView.as_view()),
    path('new_project', views.ProductListCreateAPIView.as_view()),
    path('new_task', views.TaskListCreateAPIView.as_view()),
    path('pr_request', views.PurchaseListCreateAPIView.as_view())
]