from rest_framework import serializers
from .models import List, Todo

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'title', 'user']
        read_only_fields = ['user']

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'content', 'given_list']
        read_only_fields = ['given_list']