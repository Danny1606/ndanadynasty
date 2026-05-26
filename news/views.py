from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from .forms import CustomSignupForm, CustomLoginForm, PostForm, CommentForm, EventForm
from .models import Post, Event, Comment, Like, ActivityLog, CustomUser

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.unit = form.cleaned_data.get('unit')
            user.save()
            return redirect('login')
    else:
        form = CustomSignupForm()
    return render(request, 'news/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            pin = form.cleaned_data.get('pin')
            user = authenticate(username=username, pin=pin)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'news/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def home_view(request):
    posts = Post.objects.all().order_by('-created_at').annotate(likes_count=Count('likes'))
    events = Event.objects.all().order_by('date', 'time')
    activity_logs = ActivityLog.objects.all().order_by('-timestamp')[:20]  # Recent 20 activities
    
    # Get likes for each post if user is authenticated
    user_likes = {}
    if request.user.is_authenticated:
        user_likes = set(Like.objects.filter(user=request.user, post__in=posts).values_list('post_id', flat=True))
    
    return render(request, 'news/home.html', {
        'posts': posts, 
        'events': events, 
        'user_likes': user_likes,
        'activity_logs': activity_logs
    })


def family_home_view(request):
    events = Event.objects.all().order_by('date', 'time')[:4]
    family_members = [
        {'name': 'Dspy Ndana', 'relation': 'Family Patriarch', 'bio': 'Keeping the Ndana legacy strong through love, faith, and family.', 'role': 'Founder'},
        {'name': 'Amina Ndana', 'relation': 'Family Matriarch', 'bio': 'The heart of our home, guiding every celebration and gathering.', 'role': 'Matriarch'},
        {'name': 'Juma Ndana', 'relation': 'Next Generation', 'bio': 'Bringing fresh energy, stories, and smiles to the family table.', 'role': 'Youth Ambassador'},
        {'name': 'Zuri Ndana', 'relation': 'Family Storyteller', 'bio': 'Preserving memories, photos, and family history for tomorrow.', 'role': 'Historian'},
    ]
    return render(request, 'news/family_home.html', {
        'events': events,
        'family_members': family_members,
    })


def family_about_view(request):
    return render(request, 'news/family_about.html')


def family_tree_view(request):
    return render(request, 'news/family_tree.html')


def family_contact_view(request):
    return render(request, 'news/family_contact.html')


def add_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.author = request.user
                post.author_name = request.user.get_display_name()
            else:
                post.author_name = form.cleaned_data.get('author_name') or 'Anonymous'
            post.save()
            
            # Log activity
            if request.user.is_authenticated:
                ActivityLog.objects.create(user=request.user, action='post', post=post)
            
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'news/add_news.html', {'form': form})


def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user is the author (only if post has a user author)
    if post.author and request.user != post.author:
        return redirect('home')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if not post.author and form.cleaned_data.get('author_name'):
                post.author_name = form.cleaned_data.get('author_name')
            elif request.user.is_authenticated:
                post.author_name = request.user.get_display_name()
            post.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'news/edit_news.html', {'form': form, 'post': post})


def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user is the author (only if post has a user author)
    if post.author and request.user != post.author:
        return redirect('home')
    
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'news/confirm_delete_post.html', {'post': post})


def add_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.author = request.user
                comment.author_name = request.user.get_display_name()
            else:
                comment.author_name = form.cleaned_data.get('author_name') or 'Anonymous'
            comment.save()
            
            # Log activity
            if request.user.is_authenticated:
                ActivityLog.objects.create(user=request.user, action='comment', comment=comment)
            
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'news/add_comment.html', {'form': form, 'post': post})


def edit_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user is the author (only if comment has a user author)
    if comment.author and request.user != comment.author:
        return redirect('home')
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            if not comment.author and form.cleaned_data.get('author_name'):
                comment.author_name = form.cleaned_data.get('author_name')
            elif request.user.is_authenticated:
                comment.author_name = request.user.get_display_name()
            comment.save()
            return redirect('home')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'news/edit_comment.html', {'form': form, 'comment': comment})


def delete_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user is the author (only if comment has a user author)
    if comment.author and request.user != comment.author:
        return redirect('home')
    
    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request, 'news/confirm_delete_comment.html', {'comment': comment})


@require_POST
def like_post_view(request, post_id):
    """AJAX endpoint for liking/unliking posts"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)
    
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:  # Unlike
        like.delete()
        liked = False
    else:  # Like
        liked = True
        ActivityLog.objects.create(user=request.user, action='like', post=post)
    
    likes_count = post.likes.count()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'likes_count': likes_count})
    
    return redirect('home')


def add_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            if request.user.is_authenticated:
                event.created_by = request.user
            event.save()
            
            # Log activity
            if request.user.is_authenticated:
                ActivityLog.objects.create(user=request.user, action='event', event=event)
            
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'news/add_event.html', {'form': form})
