#!/usr/bin/env python
"""Setup test users for the family website"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ndanadynasty.settings')
django.setup()

from news.models import CustomUser, Post, Event
from datetime import datetime, timedelta

# Create test family members
test_users = [
    {
        'username': 'john_family',
        'password': 'TestPass123!',
        'first_name': 'John',
        'last_name': 'Smith',
        'pin': '1234',
        'unit': 'Main House'
    },
    {
        'username': 'jane_family',
        'password': 'TestPass123!',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'pin': '5678',
        'unit': 'Main House'
    },
    {
        'username': 'mike_family',
        'password': 'TestPass123!',
        'first_name': 'Mike',
        'last_name': 'Smith',
        'pin': '9012',
        'unit': 'East Wing'
    },
    {
        'username': 'sarah_family',
        'password': 'TestPass123!',
        'first_name': 'Sarah',
        'last_name': 'Johnson',
        'pin': '3456',
        'unit': 'East Wing'
    }
]

print("Creating test users...")
for user_data in test_users:
    if not CustomUser.objects.filter(username=user_data['username']).exists():
        user = CustomUser.objects.create_user(
            username=user_data['username'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            pin=user_data['pin'],
            unit=user_data['unit']
        )
        print(f"✓ Created user: {user.username} ({user.get_display_name()})")
    else:
        print(f"⊘ User already exists: {user_data['username']}")

# Create test posts
print("\nCreating test posts...")
john = CustomUser.objects.get(username='john_family')
jane = CustomUser.objects.get(username='jane_family')

sample_posts = [
    {
        'author': john,
        'content': 'Just finished a great family dinner! Everyone was laughing and having a good time. 😊',
    },
    {
        'author': jane,
        'content': 'Check out the meme I found - totally describes us! 😂',
    },
    {
        'author': john,
        'content': 'Weekend plans: hiking at the national park. Anyone want to join?',
    },
]

for post_data in sample_posts:
    if not Post.objects.filter(author=post_data['author'], content=post_data['content']).exists():
        post = Post.objects.create(
            author=post_data['author'],
            author_name=post_data['author'].get_display_name(),
            content=post_data['content']
        )
        print(f"✓ Created post from {post.author.first_name}")
    else:
        print(f"⊘ Similar post already exists")

# Create test event
print("\nCreating test events...")
if not Event.objects.filter(title='Family Reunion 2026').exists():
    event = Event.objects.create(
        title='Family Reunion 2026',
        date=datetime.now().date() + timedelta(days=30),
        time=datetime.now().time(),
        description='Annual family reunion - bring your family and friends!',
        location='Central Park',
        created_by=john
    )
    print(f"✓ Created event: {event.title}")
else:
    print("⊘ Event already exists")

print("\n✓ Setup complete!")
print("\nTest user credentials:")
for user_data in test_users:
    print(f"  Username: {user_data['username']}, PIN: {user_data['pin']}")
