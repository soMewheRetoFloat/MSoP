from django.urls import path
from . import views

app_name = 'news'
urlpatterns = [
    path('', views.index, name='index'),
    path('article/<int:pk>/', views.detail, name='detail'),
    path('add_comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('del_comment/<int:pk>/<int:comid>/', views.del_comment, name='del_comment'),
    path('list/', views.news_list, name='news_list'),
    path('category_list/', views.category_list, name='category_list'),
    path('category_list/<int:pk>/', views.category_detail, name='category_detail'),
    path('search/', views.search, name='search')
]
