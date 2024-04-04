from django.contrib import admin
from .models import News, Comment, Category

# Register your models here.

admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Category)