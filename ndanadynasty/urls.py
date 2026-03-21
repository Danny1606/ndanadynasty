from django.contrib import admin
from django.urls import path
from .views import home

urlpatterns = [
    path("", home),  # homepage route
    path("admin/", admin.site.urls),
]
