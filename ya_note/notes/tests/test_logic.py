from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify

from .basecase import (BaseCase, FORM_DATA, URL_ADD_NOTE,
                       URL_SUCCESS, URL_DELETE, URL_EDIT_NOTE,
                       OTHER_SLUG, redirect_url)
from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestNoteCreation(BaseCase):

    def test_auth_user_can_create_note(self):
        old_notes = set(Note.objects.all())
        response = self.author_client.post(
            URL_ADD_NOTE, data=dict(**FORM_DATA, slug=OTHER_SLUG))
        self.assertRedirects(response, URL_SUCCESS)
        new_notes_set = set(Note.objects.all()) - old_notes
        self.assertEqual(len(new_notes_set), 1)
        new_note = new_notes_set.pop()
        self.assertEqual(new_note.title, FORM_DATA['title'])
        self.assertEqual(new_note.text, FORM_DATA['text'])
        self.assertEqual(new_note.author, self.author)
        self.assertEqual(new_note.slug, OTHER_SLUG)

    def test_create_note_with_no_slug(self):
        old_notes = set(Note.objects.all())
        response = self.author_client.post(URL_ADD_NOTE, data=FORM_DATA)
        self.assertRedirects(response, URL_SUCCESS)
        new_notes = set(Note.objects.all()) - old_notes
        self.assertEqual(len(new_notes), 1)
        new_note = new_notes.pop()
        self.assertEqual(new_note.title, FORM_DATA['title'])
        self.assertEqual(new_note.text, FORM_DATA['text'])
        self.assertEqual(new_note.author, self.author)
        self.assertEqual(new_note.slug, slugify(FORM_DATA['title']))

    def test_anonymous_user_cant_create_note(self):
        expected_notes = tuple(Note.objects.all())
        response = self.client.post(URL_ADD_NOTE, data=FORM_DATA)
        self.assertRedirects(response, redirect_url(URL_ADD_NOTE))
        self.assertEqual(tuple(Note.objects.all()), expected_notes)

    def test_not_unique_slug(self):
        expected_notes = tuple(Note.objects.all())
        response = self.author_client.post(
            URL_ADD_NOTE, data=dict(**FORM_DATA, slug=self.note.slug))
        self.assertFormError(
            response, 'form', 'slug', errors=(self.note.slug + WARNING))
        self.assertEqual(tuple(Note.objects.all()), expected_notes)

    def test_author_can_edit_note(self):
        not_edit_note = self.note
        response = self.author_client.post(URL_EDIT_NOTE, data=FORM_DATA)
        self.assertRedirects(response, URL_SUCCESS)
        edit_note = Note.objects.get(id=not_edit_note.id)
        self.assertEqual(edit_note.title, FORM_DATA['title'])
        self.assertEqual(edit_note.text, FORM_DATA['text'])
        self.assertEqual(edit_note.slug, slugify(FORM_DATA['title']))
        self.assertEqual(edit_note.author, not_edit_note.author)

    def test_author_can_delete_note(self):
        expected_notes_set = set(Note.objects.all()) - {self.note}
        response = self.author_client.delete(URL_DELETE)
        self.assertRedirects(response, URL_SUCCESS)
        self.assertEqual(set(Note.objects.all()), expected_notes_set)

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
        expected_notes = tuple(Note.objects.all())
        response = self.other_author_client.delete(URL_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(tuple(Note.objects.all()), expected_notes)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.author, note_from_db.author)
        self.assertEqual(self.note.slug, note_from_db.slug)
