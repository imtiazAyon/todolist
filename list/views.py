from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from .models import List, Todo
from .serializers import ListSerializer, TodoSerializer
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer


class UserIsListCreatorMixin:
     """Verify that the current user is the creator of the list."""
     def dispatch(self, request, *args, **kwargs):
        try:
            id = int(self.kwargs['pk'])
            given_list = List.objects.get(id=id)
        except  ObjectDoesNotExist:
            raise Http404
        if given_list.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class SignupView(APIView):
    """Register a new user"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registration/signup.html'
    def get(self, request, format=None, **kwargs):
        form = UserCreationForm()
        return Response({'form':form})
    def post(self, request, format=None, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return redirect('signup')

class ShowUserLists(APIView):
    """Show all the list the current user created."""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'list/user_lists.html'
    def get(self, request, format=None, **kwargs):
        user=request.user
        if not user.is_authenticated:
            return redirect('login')
        lists = List.objects.filter(user=user)
        serializer = ListSerializer(lists, many=True)
        return Response({'user':user, 'user_lists':serializer.data})

class CreateList(APIView):
    """Creates a new list."""
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None, **kwargs):
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return redirect("user_lists")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteList(APIView):
    """Deletes a list if the current user is the list creator"""
    def post(self, request, format=None, **kwargs):
        id = int(request.query_params.get("list_id"))
        given_list = List.objects.get(id=id)
        if given_list.user != request.user:
            raise PermissionDenied
        given_list.delete()
        return redirect("user_lists")

class ViewTodo(UserIsListCreatorMixin, APIView):
    """Views all the todos in a list to the list creator"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'list/list_detail.html'

    def get_objects(self):
        try:
            id = int(self.kwargs['pk'])
            return List.objects.get(id=id)
        except ObjectDoesNotExist:
            raise Http404
        

    def get(self, request, format=None, **kwargs):
        given_list = self.get_objects()
        todos = Todo.objects.filter(given_list=given_list)
        serializer = TodoSerializer(todos, many=True)
        #return Response(serializer.data)
        return Response({'given_list':given_list, 'todos':serializer.data})


class DeleteTodo(UserIsListCreatorMixin, APIView):
    """Deletes a todo if the current user is the list creator"""
    def post(self, request, format=None, **kwargs):
        try:
            id = int(request.query_params.get("todo_id"))
            todo = Todo.objects.get(id=id)
            todo.delete()
            return redirect("list_detail", pk=self.kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404

class CreateTodo(UserIsListCreatorMixin, APIView):
    """Creates a todo if the current user is the list creator"""
    def post(self, request, format=None, **kwargs):
        try:
            id = int(self.kwargs['pk'])
            given_list = List.objects.get(id=id)
        except ObjectDoesNotExist:
            raise Http404
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(given_list=given_list)
            return redirect("list_detail", pk=self.kwargs['pk'])
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)