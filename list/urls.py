from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.Show_Lists.as_view()),
    path('<int:pk>', views.ViewUpdateDeleteTodo.as_view()),
    path('<int:pk>/', views.ViewUpdateDeleteTodo.as_view()),
]