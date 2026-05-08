from django.shortcuts import render, get_object_or_404, redirect
from .models import FamilyNews, Comment, Notification
from .forms import FamilyNewsForm, CommentForm, NotificationForm

def home(request):
    family_news = FamilyNews.objects.order_by('-created_at')
    notifications = Notification.objects.order_by('-date')
    comment_form = CommentForm()

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            post_id = request.POST.get('post_id')
            post = get_object_or_404(FamilyNews, id=post_id)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                return redirect('home')

    return render(request, 'news/home.html', {
        'family_news': family_news,
        'notifications': notifications,
        'comment_form': comment_form,
        'form': FamilyNewsForm(),
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

def edit_news(request, pk):
    post = get_object_or_404(FamilyNews, pk=pk)
    if request.method == 'POST':
        form = FamilyNewsForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FamilyNewsForm(instance=post)
    return render(request, 'news/edit_news.html', {'form': form})

def delete_news(request, pk):
    post = get_object_or_404(FamilyNews, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'news/delete_news.html', {'post': post})

def add_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NotificationForm()
    return render(request, 'news/add_notification.html', {'form': form})

def edit_notification(request, pk):
    note = get_object_or_404(Notification, pk=pk)
    if request.method == 'POST':
        form = NotificationForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NotificationForm(instance=note)
    return render(request, 'news/edit_notification.html', {'form': form})

def delete_notification(request, pk):
    note = get_object_or_404(Notification, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('home')
    return render(request, 'news/delete_notification.html', {'note': note})
