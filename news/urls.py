from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.family_home_view, name='home'),
    path('community/', views.home_view, name='news_home'),
    path('family/', views.family_home_view, name='family_home'),
    path('family/about/', views.family_about_view, name='family_about'),
    path('family/tree/', views.family_tree_view, name='family_tree'),
    path('family/contact/', views.family_contact_view, name='family_contact'),
    
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
]
