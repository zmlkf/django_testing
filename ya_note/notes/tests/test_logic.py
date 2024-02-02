from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify

from .basecase import BaseCase
from .constants_urls import (
    FORM_DATA, URL_ADD_NOTE, URL_SUCCESS,
    URL_LOGIN, URL_DELETE, URL_EDIT_NOTE, SLUG)
from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestNoteCreation(BaseCase):

    def test_empty_slug_and_auth_user_can_create_note(self):
        notes_count = Note.objects.count()
        response = self.author_client.post(URL_ADD_NOTE, data=FORM_DATA)
        self.assertRedirects(response, URL_SUCCESS)
        self.assertEqual(Note.objects.count(), notes_count + 1)
        new_note = Note.objects.last()
        self.assertEqual(new_note.title, FORM_DATA['title'])
        self.assertEqual(new_note.text, FORM_DATA['text'])
        self.assertEqual(new_note.author, self.author)
        self.assertEqual(new_note.slug, slugify(FORM_DATA['title']))

    def test_anonymous_user_cant_create_note(self):
        notes_count = Note.objects.count()
        response = self.client.post(URL_ADD_NOTE, data=FORM_DATA)
        self.assertRedirects(response, f'{URL_LOGIN}?next={URL_ADD_NOTE}')
        self.assertEqual(Note.objects.count(), notes_count)

    def test_not_unique_slug(self):
        notes_count = Note.objects.count()
        response = self.author_client.post(
            URL_ADD_NOTE, data=dict(**FORM_DATA, slug=SLUG))
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(SLUG + WARNING)
        )
        self.assertEqual(Note.objects.count(), notes_count)

    def test_author_can_edit_note(self):
        response = self.author_client.post(URL_EDIT_NOTE, data=FORM_DATA)
        self.assertRedirects(response, URL_SUCCESS)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, FORM_DATA['title'])
        self.assertEqual(self.note.text, FORM_DATA['text'])
        self.assertEqual(self.note.slug, slugify(FORM_DATA['title']))
        self.assertEqual(self.note.author, self.author)

    def test_author_can_delete_note(self):
        notes_count = Note.objects.count()
        response = self.author_client.delete(URL_DELETE)
        self.assertRedirects(response, URL_SUCCESS)
        self.assertEqual(Note.objects.count(), notes_count - 1)

    def test_not_author_client_cant_edit_note(self):
        response = self.other_author_client.post(
            URL_EDIT_NOTE, data=FORM_DATA)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.author, note_from_db.author)
        self.assertEqual(self.note.slug, note_from_db.slug)

    def test_not_author_client_cant_delete_note(self):
        notes_count = Note.objects.count()
        response = self.other_author_client.delete(URL_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), notes_count)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.author, note_from_db.author)
        self.assertEqual(self.note.slug, note_from_db.slug)
