from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note

User = get_user_model()

SLUG = 'slug'

URL_HOME = reverse('notes:home')
URL_NOTES_LIST = reverse('notes:list')
URL_ADD_NOTE = reverse('notes:add')
URL_SUCCESS = reverse('notes:success')
URL_DETAIL = reverse('notes:detail', args=(SLUG,))
URL_EDIT_NOTE = reverse('notes:edit', args=(SLUG,))
URL_DELETE = reverse('notes:delete', args=(SLUG,))

URL_LOGIN = reverse('users:login')
URL_LOGOUT = reverse('users:logout')
URL_SIGNUP = reverse('users:signup')

FORM_DATA = {'title': 'Заголовок', 'text': 'Текст'}
FORM_DATA_WITH_SLUG = {'title': 'Заголовок', 'text': 'Текст', 'slug': '_slug'}


def redirect_url(url):
    return f'{URL_LOGIN}?next={url}'


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
            title='title',
            text='text',
            author=cls.author,
            slug=SLUG
        )
