from django.shortcuts import render
#from django.http import HttpResponse
from .models import List, Todo
from .serializers import ListSerializer, TodoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


#from rest_framework import generics


# Create your views here.
#def home(request):
#      return HttpResponse("Hello World!")

class Show_Lists(APIView):

    def get(self, request, format=None, **kwargs):
        lists = List.objects.all()
        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)

class ViewUpdateDeleteTodo(APIView):

    def get_objects(self):
        id = int(self.kwargs['pk'])
        return List.objects.get(id=id)
        

    def get(self, request, format=None, **kwargs):
        given_list = self.get_objects()
        todos = Todo.objects.filter(given_list=given_list)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def put(self, request, format=None, **kwargs):

        if "todo_id" in request.query_params:
            id = int(request.query_params.get("todo_id"))
            todo = Todo.objects.get(id=id)
            serializer = TodoSerializer(todo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        else:
            given_list = self.get_objects()
            serializer = TodoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(given_list=given_list)
                return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None, **kwargs):
        id = int(request.query_params.get("todo_id"))
        todo = Todo.objects.get(id=id)
        todo.delete()
        return Response({'message':'Todo deleted'})

