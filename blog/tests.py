from django.test import TestCase
from django.contrib.auth.models import User
from .models import Blog

# Create your tests here.

class BlogTest(TestCase):

    def setUp(self):

        user = User.objects.create_user(username='ahmed',password='ahmed123456789')
        user.save()

        blog = Blog.objects.create(author=user,title='first title',body='first body')
        blog.save()

    def test_blog(self):

        blog = Blog.objects.get(id=1)
        self.assertEqual(blog.author.username, 'ahmed')
        self.assertEqual(blog.title, 'first title')
        self.assertEqual(blog.body, 'first body')
