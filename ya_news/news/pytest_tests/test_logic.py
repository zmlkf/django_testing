from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


FORM_DATA = {'text': 'Новый комментарий'}
BAD_FORM_DATA = {'text': f'Текст {BAD_WORDS[0]}'}


def test_anonymous_user_cant_create_note(client, detail_url, redirect_url):
    expected_comments = tuple(Comment.objects.all())
    assertRedirects(
        client.post(detail_url, data=FORM_DATA), redirect_url(detail_url))
    assert tuple(Comment.objects.all()) == expected_comments


def test_autorized_user_can_create_comment(
    author_client, author, news, detail_url
):
    old_comments = set(Comment.objects.all())
    response = author_client.post(detail_url, data=FORM_DATA)
    assertRedirects(response, f'{detail_url}#comments')
    new_comments = (set(Comment.objects.all()) - old_comments)
    assert len(new_comments) == 1
    new_comment = new_comments.pop()
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.author == author
    assert new_comment.news == news


def test_user_cant_use_bad_words(author_client, detail_url):
    expected_comments = tuple(Comment.objects.all())
    response = author_client.post(detail_url, data=BAD_FORM_DATA)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert tuple(Comment.objects.all()) == expected_comments


def test_author_can_edit_comment(
        author_client, author, comment, news, edit_url, detail_url):
    response = author_client.post(edit_url, data=FORM_DATA)
    assertRedirects(response, f'{detail_url}#comments')
    comment.refresh_from_db()
    assert comment.text == FORM_DATA['text']
    assert comment.author == author
    assert comment.news == news


def test_author_can_delete_comment(
        author_client, comment, detail_url, delete_url):
    expected_comments = set(Comment.objects.all()) - {comment}
    assertRedirects(
        author_client.delete(delete_url), f'{detail_url}#comments')
    assert set(Comment.objects.all()) == expected_comments


def test_user_cant_edit_comment_of_another_user(
        not_author_client, comment, edit_url):
    old_comment = comment
    assert not_author_client.post(
        edit_url, data=FORM_DATA).status_code == HTTPStatus.NOT_FOUND
    assert comment == old_comment


def test_user_cant_delete_comment_of_another_user(
        not_author_client, comment, delete_url):
    comments = tuple(Comment.objects.all())
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert tuple(Comment.objects.all()) == comments
