from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Пользователь1')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author
        )
        cls.other_author = User.objects.create(username='Пользователь2')

    def test_notes_list_for_different_users(self):
        users = (
            (self.author, True),
            (self.other_author, False),
        )
        url = reverse('notes:list',)
        for user, value in users:
            self.client.force_login(user)
            with self.subTest(user=user, value=value):
                response = self.client.get(url)
                object_list = response.context['object_list']
                self.assertEqual(self.note in object_list, value)

    def test_pages_edit_and_add_has_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        for name, args in urls:
            self.client.force_login(self.author)
            with self.subTest(name=name, args=args):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
