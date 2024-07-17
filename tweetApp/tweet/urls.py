from . import views
from django.urls import path

urlpatterns = [
    path('', views.list_tweet, name='list_tweet'),
    path('create/', views.create_tweet, name='create_tweet'),
    path('<int:tweet_id>/edit/', views.edit_tweet, name='edit_tweet'),
    path('<int:tweet_id>/delete/', views.delete_tweet, name='delete_tweet'),
    path('register/', views.register, name='register'),
    path('search/', views.search_view, name='search'),
] 
