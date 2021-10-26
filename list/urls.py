from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.ShowAllLists.as_view()),
    path('create/', views.CreateList.as_view()),
    path('user/', views.ShowUserLists.as_view()),
    path('<int:pk>', views.ViewUpdateDeleteTodo.as_view()),
    path('<int:pk>/', views.ViewUpdateDeleteTodo.as_view()),
]