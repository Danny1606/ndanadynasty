from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add-news/", views.add_news, name="add_news"),
    path("edit-news/<int:pk>/", views.edit_news, name="edit_news"),
    path("delete-news/<int:pk>/", views.delete_news, name="delete_news"),
    path("add-notification/", views.add_notification, name="add_notification"),
    path("delete-notification/<int:pk>/", views.delete_notification, name="delete_notification"),
]
