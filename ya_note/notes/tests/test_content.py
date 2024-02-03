from django.contrib.auth import get_user_model

from .basecase import URL_ADD_NOTE, URL_EDIT_NOTE, URL_NOTES_LIST, BaseCase
from notes.forms import NoteForm

User = get_user_model()


class TestContent(BaseCase):

    def test_note_in_notes_list_for_author(self):
        note = self.author_client.get(
            URL_NOTES_LIST).context['object_list'].get(id=self.note.id)
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
                response = self.author_client.get(url)
                self.assertIsInstance(response.context.get('form'), NoteForm)
