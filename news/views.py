from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from .forms import PostForm, CommentForm, EventForm
from .models import Post, Event, Comment, Like, ActivityLog

def _get_user_likes(request):
    if request.user.is_authenticated:
        return set(Like.objects.filter(author_name=request.user.username).values_list('post_id', flat=True))
    return set()


def _get_feed_context(request):
    posts = Post.objects.all().order_by('-created_at').annotate(likes_count=Count('likes'))
    events = Event.objects.all().order_by('date', 'time')
    activity_logs = ActivityLog.objects.all().order_by('-timestamp')[:20]
    return {
        'posts': posts,
        'events': events,
        'activity_logs': activity_logs,
        'user_likes': _get_user_likes(request),
    }


def home_view(request):
    context = _get_feed_context(request)
    return render(request, 'news/home.html', context)


def public_feed_view(request):
    context = _get_feed_context(request)
    return render(request, 'news/public_home.html', context)


def family_home_view(request):
    events = Event.objects.all().order_by('date', 'time')[:4]
    family_members = [
        {
            'name': 'Ndana',
            'relation': 'Family Patriarch',
            'bio': 'Keeping the Ndana legacy strong through love, faith, and family.',
            'role': 'Founder',
            'image': '/media/post_images/1000098804.jpg',
        },
        {
            'name': 'Mbathi',
            'relation': 'Family Matriarch',
            'bio': 'The heart of our home, guiding every celebration and gathering.',
            'role': 'Matriarch',
            'image': '/media/post_images/1000098804_OyMQsxJ.jpg',
        },
        {
            'name': 'Dspy',
            'relation': 'Youth Ambassador',
            'bio': 'Bringing fresh energy, stories, and smiles to the family table.',
            'role': 'Youth Ambassador',
            'image': '/media/post_images/1000098804_b2NFqnE.jpg',
        },
        {
            'name': 'Gypsy',
            'relation': 'Family Storyteller',
            'bio': 'Preserving memories, photos, and family history for tomorrow.',
            'role': 'Storyteller',
            'image': '/media/post_images/1000098804.jpg',
        },
    ]
    return render(request, 'news/family_home.html', {
        'events': events,
        'family_members': family_members,
    })

def family_about_view(request):
    return render(request, 'news/family_about.html')

def family_contact_view(request):
    return render(request, 'news/family_contact.html')

def add_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author_name = form.cleaned_data.get('author_name') or 'Anonymous'
            post.save()
            ActivityLog.objects.create(author_name=post.author_name, action='post', post=post)
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'news/add_news.html', {'form': form})

def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author_name = form.cleaned_data.get('author_name') or post.author_name
            post.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'news/edit_news.html', {'form': form, 'post': post})

def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
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
            comment.author_name = form.cleaned_data.get('author_name') or 'Anonymous'
            comment.save()
            ActivityLog.objects.create(author_name=comment.author_name, action='comment', comment=comment)
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'news/add_comment.html', {'form': form, 'post': post})

def edit_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author_name = form.cleaned_data.get('author_name') or comment.author_name
            comment.save()
            return redirect('home')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'news/edit_comment.html', {'form': form, 'comment': comment})

def delete_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request, 'news/confirm_delete_comment.html', {'comment': comment})

@require_POST
def like_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    author_name = request.user.username if request.user.is_authenticated else "Guest"
    like, created = Like.objects.get_or_create(post=post, author_name=author_name)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
        ActivityLog.objects.create(author_name=author_name, action='like', post=post)
    likes_count = post.likes.count()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'likes_count': likes_count})
    return redirect('home')

def add_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            ActivityLog.objects.create(author_name="Guest", action='event', event=event)
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'news/add_event.html', {'form': form})
