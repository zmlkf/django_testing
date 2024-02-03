from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify

from .basecase import (
    BaseCase, FORM_DATA, FORM_DATA_WITH_SLUG,
    URL_ADD_NOTE, URL_SUCCESS, URL_DELETE,
    URL_EDIT_NOTE, redirect_url
)
from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestNoteCreation(BaseCase):

    def create_note(self, form_data):
        notes = set(Note.objects.all())
        self.assertRedirects(self.author_client.post(
            URL_ADD_NOTE, data=form_data), URL_SUCCESS)
        notes = set(Note.objects.all()) - notes
        self.assertEqual(len(notes), 1)
        new_note = notes.pop()
        self.assertEqual(new_note.title, form_data['title'])
        self.assertEqual(new_note.text, form_data['text'])
        self.assertEqual(new_note.author, self.author)
        self.assertEqual(new_note.slug, form_data.get(
            'slug') or slugify(FORM_DATA['title']))

    def test_auth_user_can_create_note(self):
        self.create_note(FORM_DATA_WITH_SLUG)

    def test_create_note_with_no_slug(self):
        self.create_note(FORM_DATA)

    def test_anonymous_user_cant_create_note(self):
        expected_notes = set(Note.objects.all())
        print(expected_notes)
        response = self.client.post(URL_ADD_NOTE, data=FORM_DATA)
        self.assertRedirects(response, redirect_url(URL_ADD_NOTE))
        self.assertEqual(set(Note.objects.all()), expected_notes)

    def test_not_unique_slug(self):
        expected_notes = set(Note.objects.all())
        print(expected_notes)
        response = self.author_client.post(
            URL_ADD_NOTE, data=dict(**FORM_DATA, slug=self.note.slug))
        self.assertFormError(
            response, 'form', 'slug', errors=(self.note.slug + WARNING))
        self.assertEqual(set(Note.objects.all()), expected_notes)

    def test_author_can_edit_note(self):
        self.assertRedirects(
            self.author_client.post(URL_EDIT_NOTE, data=FORM_DATA_WITH_SLUG),
            URL_SUCCESS
        )
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, FORM_DATA_WITH_SLUG['title'])
        self.assertEqual(note.text, FORM_DATA_WITH_SLUG['text'])
        self.assertEqual(note.slug, FORM_DATA_WITH_SLUG['slug'])
        self.assertEqual(note.author, self.note.author)

    def test_author_can_delete_note(self):
        notes_count = Note.objects.count()
        response = self.author_client.delete(URL_DELETE)
        self.assertRedirects(response, URL_SUCCESS)
        self.assertEqual(Note.objects.count(), notes_count - 1)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_not_author_client_cant_edit_note(self):
        response = self.other_author_client.post(
            URL_EDIT_NOTE, data=FORM_DATA)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.author, note.author)
        self.assertEqual(self.note.slug, note.slug)

    def test_not_author_client_cant_delete_note(self):
        notes_count = Note.objects.count()
        response = self.other_author_client.delete(URL_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), notes_count)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.author, note.author)
        self.assertEqual(self.note.slug, note.slug)
