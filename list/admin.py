from django.contrib import admin

# Register your models here.

from .models import List, Todo

admin.site.register(List)
admin.site.register(Todo)