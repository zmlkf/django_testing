from django.contrib.auth import get_user_model

from .basecase import BaseCase
from .constants_urls import (SLUG, TEXT, TITLE, URL_ADD_NOTE, URL_EDIT_NOTE,
                             URL_NOTES_LIST)
from notes.forms import NoteForm

User = get_user_model()


class TestContent(BaseCase):

    def test_note_in_notes_list_for_author(self):
        response = self.author_client.get(URL_NOTES_LIST)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)
        note = object_list.get(slug=SLUG)
        self.assertEqual(note.title, TITLE)
        self.assertEqual(note.text, TEXT)
        self.assertEqual(note.author, self.author)

    def test_note_not_in_notes_list_for_other_author(self):
        object_list = self.other_author_client.get(
            URL_NOTES_LIST).context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_pages_edit_and_add_has_form(self):
        for url in (URL_ADD_NOTE, URL_EDIT_NOTE):
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
