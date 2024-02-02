from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from .constants_urls import SLUG, TEXT, TITLE
from notes.models import Note

User = get_user_model()


class BaseCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Пользователь1')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.other_author = User.objects.create(username='Пользователь2')
        cls.other_author_client = Client()
        cls.other_author_client.force_login(cls.other_author)
        cls.note = Note.objects.create(
            title=TITLE,
            text=TEXT,
            author=cls.author,
            slug=SLUG
        )
