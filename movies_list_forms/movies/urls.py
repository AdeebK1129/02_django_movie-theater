from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('list_view/', views.list_view, name='list_view'),
    path('create_view/', views.create_view, name='create_view'),
    path('edit_view/<int:movie_id>/', views.edit_view, name='edit_view'),
    path('delete_view/<int:movie_id>/', views.delete_view, name='delete_view'),
    path('deleteConfirm_view/<int:movie_id>/', views.deleteConfirm_view, name='deleteConfirm_view'),
] 
