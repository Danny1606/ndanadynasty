from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import FamilyNews, Notification
from .forms import FamilyNewsForm, NotificationForm

def home(request):
    family_news = FamilyNews.objects.all().order_by("-id")
    notifications = Notification.objects.filter(date__gte=now().date()).order_by("date")
    return render(request, "news/home.html", {
        "family_news": family_news,
        "notifications": notifications,
        "form": FamilyNewsForm(),
        "notification_form": NotificationForm(),
        "today": now().date(),
    })

def add_news(request):
    if request.method == "POST":
        form = FamilyNewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            print(form.errors)  # debug
    return redirect("home")

def edit_news(request, pk):
    news = get_object_or_404(FamilyNews, pk=pk)
    if request.method == "POST":
        form = FamilyNewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "news/add_post.html", {"form": form})

def delete_news(request, pk):
    news = get_object_or_404(FamilyNews, pk=pk)
    if request.method == "POST":
        news.delete()
        return redirect("home")
    return render(request, "news/confirm_delete.html", {"object": news})

def add_notification(request):
    if request.method == "POST":
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            print(form.errors)  # debug
    return redirect("home")

def delete_notification(request, pk):
    note = get_object_or_404(Notification, pk=pk)
    if request.method == "POST":
        note.delete()
        return redirect("home")
    return render(request, "news/confirm_delete.html", {"object": note})
