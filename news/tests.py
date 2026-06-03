from django.test import TestCase, Client
from django.urls import reverse
from .models import Post, Comment
from .forms import PostForm, CommentForm


class PostFormTest(TestCase):
    def test_post_form_valid_with_optional_author(self):
        form = PostForm(data={'author_name': 'Test User', 'content': 'Hello family'})
        self.assertTrue(form.is_valid())

    def test_post_form_valid_without_author(self):
        form = PostForm(data={'content': 'Anonymous post'})
        self.assertTrue(form.is_valid())


class CommentFormTest(TestCase):
    def test_comment_form_valid_with_optional_author(self):
        form = CommentForm(data={'author_name': 'Commenter', 'text': 'Nice post!'})
        self.assertTrue(form.is_valid())

    def test_comment_form_valid_without_author(self):
        form = CommentForm(data={'text': 'Anonymous comment'})
        self.assertTrue(form.is_valid())


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.post = Post.objects.create(author_name='Tester', content='Home view test')

    def test_home_view_renders(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/home.html')
        self.assertContains(response, 'Home view test')

    def test_public_feed_view_renders(self):
        response = self.client.get(reverse('public_feed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/public_home.html')
        self.assertContains(response, 'Home view test')
