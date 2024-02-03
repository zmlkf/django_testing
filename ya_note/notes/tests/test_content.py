from django.contrib.auth import get_user_model

from .basecase import URL_ADD_NOTE, URL_EDIT_NOTE, URL_NOTES_LIST, BaseCase
from notes.forms import NoteForm

User = get_user_model()


class TestContent(BaseCase):

    def test_note_in_notes_list_for_author(self):
        notes = self.author_client.get(URL_NOTES_LIST).context['object_list']
        self.assertIn(self.note, notes)
        note = notes.get(id=self.note.id)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.author, note.author)
        self.assertEqual(self.note.slug, note.slug)

    def test_note_not_in_notes_list_for_other_author(self):
        self.assertNotIn(self.note, self.other_author_client.get(
            URL_NOTES_LIST).context['object_list'])

    def test_pages_edit_and_add_has_form(self):
        for url in (URL_ADD_NOTE, URL_EDIT_NOTE):
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_client.get(url).context.get('form'),
                    NoteForm
                )
