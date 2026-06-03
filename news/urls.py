from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('public/', views.public_feed_view, name='public_feed'),

    # Post URLs
    path('add-post/', views.add_post_view, name='add_post'),
    path('edit-post/<int:post_id>/', views.edit_post_view, name='edit_post'),
    path('delete-post/<int:post_id>/', views.delete_post_view, name='delete_post'),

    # Comment URLs
    path('add-comment/<int:post_id>/', views.add_comment_view, name='add_comment'),
    path('edit-comment/<int:comment_id>/', views.edit_comment_view, name='edit_comment'),
    path('delete-comment/<int:comment_id>/', views.delete_comment_view, name='delete_comment'),

    # Like URL
    path('like-post/<int:post_id>/', views.like_post_view, name='like_post'),

    # Event URLs
    path('add-event/', views.add_event_view, name='add_event'),
    path('edit-event/<int:event_id>/', views.edit_event_view, name='edit_event'),
    path('delete-event/<int:event_id>/', views.delete_event_view, name='delete_event'),

    # Family pages (keep About + Contact, remove Tree)
    path('family/home/', views.family_home_view, name='family_home'),
    path('family/about/', views.family_about_view, name='family_about'),
    path('family/contact/', views.family_contact_view, name='family_contact'),
]
