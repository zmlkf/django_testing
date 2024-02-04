from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


FORM_DATA = {'text': 'Новый комментарий'}
BAD_FORM_DATA = {'text': f'Текст {BAD_WORDS[0]}'}


def test_anonymous_cant_create_comment(client, detail_url, redirect_detail):
    assertRedirects(
        client.post(detail_url, data=FORM_DATA), redirect_detail)
    assert Comment.objects.count() == 0


def test_autorized_user_can_create_comment(
        author_client, author, news, detail_url):
    assertRedirects(
        author_client.post(detail_url, data=FORM_DATA),
        f'{detail_url}#comments'
    )
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.author == author
    assert comment.news == news


def test_user_cant_use_bad_words(author_client, detail_url):
    response = author_client.post(detail_url, data=BAD_FORM_DATA)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(
        author_client, comment, edit_url, detail_url):
    response = author_client.post(edit_url, data=FORM_DATA)
    assertRedirects(response, f'{detail_url}#comments')
    edit_comment = Comment.objects.get(id=comment.id)
    assert edit_comment.text == FORM_DATA['text']
    assert edit_comment.author == comment.author
    assert edit_comment.news == comment.news


def test_author_can_delete_comment(
        author_client, comment, detail_url, delete_url):
    comments_count = Comment.objects.count()
    assertRedirects(
        author_client.delete(delete_url), f'{detail_url}#comments')
    assert Comment.objects.count() == comments_count - 1
    assert not Comment.objects.filter(id=comment.id).exists()


def test_user_cant_edit_comment_of_another_user(
        not_author_client, comment, edit_url):
    assert not_author_client.post(
        edit_url, data=FORM_DATA).status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == comment.text
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news


def test_user_cant_delete_comment_of_another_user(
        not_author_client, comment, delete_url):
    comments_count = Comment.objects.count()
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_count
    assert Comment.objects.filter(
        id=comment.id,
        text=comment.text,
        author=comment.author,
        news=comment.news
    ).exists()
