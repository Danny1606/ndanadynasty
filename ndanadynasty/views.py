from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import FamilyNews, Comment, Notification
from .forms import FamilyNewsForm, CommentForm, NotificationForm

def home(request):
    posts = FamilyNews.objects.all().order_by('-created_at')
    events = Notification.objects.all().order_by('date')
    form = FamilyNewsForm()
    return render(request, 'news/home.html', {
        'form': form,
        'posts': posts,
        'events': events
    })

def add_news(request):
    if request.method == 'POST':
        form = FamilyNewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FamilyNewsForm()
    return render(request, 'news/add_news.html', {'form': form})

def add_comment(request, post_id):
    post = get_object_or_404(FamilyNews, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'news/add_comment.html', {'form': form, 'post': post})

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user.username != comment.author:
        return HttpResponseForbidden("You can only edit your own comments.")
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'news/edit_comment.html', {'form': form})

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user.username != comment.author:
        return HttpResponseForbidden("You can only delete your own comments.")
    if request.method == 'POST':
        comment.delete()
        return redirect('home')

def add_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NotificationForm()
    return render(request, 'news/add_notification.html', {'form': form})
