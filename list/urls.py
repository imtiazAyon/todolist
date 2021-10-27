from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('create/', views.CreateList.as_view()),
    path('delete', views.DeleteList.as_view()),
    path('<int:pk>/', views.ViewTodo.as_view(), name="list_detail"),
    path('<int:pk>/delete', views.DeleteTodo.as_view()),
    path('<int:pk>/create', views.CreateTodo.as_view()),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('', views.ShowUserLists.as_view(), name="user_lists"),
]