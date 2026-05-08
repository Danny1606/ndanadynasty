from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path("", views.home, name="home"),

    # Family News (Posts)
    path("add-news/", views.add_news, name="add_news"),
    path("edit-news/<int:pk>/", views.edit_news, name="edit_news"),
    path("delete-news/<int:pk>/", views.delete_news, name="delete_news"),

    # Notifications (Events)
    path("add-notification/", views.add_notification, name="add_notification"),
    path("edit-notification/<int:pk>/", views.edit_notification, name="edit_notification"),
    path("delete-notification/<int:pk>/", views.delete_notification, name="delete_notification"),
]
