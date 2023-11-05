from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('create_view/', views.create_view, name='create_view'), 
    path('edit_view/', views.edit_view, name='edit_view'), 
    path('list_view/', views.list_view, name='list_view'), 
]