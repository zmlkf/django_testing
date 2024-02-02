from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db

FORM_DATA = {'text': 'Комментарий'}


def test_anonymous_user_cant_create_note(client, url_detail, redirect_login):
    comment_count = Comment.objects.count()
    response = client.post(url_detail, data=FORM_DATA)
    expected_url = redirect_login + url_detail
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == comment_count


def test_autorized_user_can_create_comment(
    author_client, author, news, url_detail
):
    comment_count = Comment.objects.count()
    response = author_client.post(url_detail, data=FORM_DATA)
    expected_url = f'{url_detail}#comments'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == comment_count + 1
    new_comment = Comment.objects.get()
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.author == author
    assert new_comment.news == news


@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_user_cant_use_bad_words(author_client, bad_word, url_detail):
    comment_count = Comment.objects.count()
    bad_words_data = {'text': f'Текст {bad_word} текст'}
    response = author_client.post(url_detail, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == comment_count


def test_author_can_edit_comment(author_client, comment, url_edit, url_detail):
    response = author_client.post(
        url_edit, data=FORM_DATA)
    url_to_comments = f'{url_detail}#comments'
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == FORM_DATA['text']


def test_author_can_delete_comment(
        author_client, comment, url_detail, url_delete):
    comment_count = Comment.objects.count()
    response = author_client.delete(url_delete)
    url_to_comments = f'{url_detail}#comments'
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == comment_count - 1


def test_user_cant_edit_comment_of_another_user(
        not_author_client, comment, url_edit):
    old_comment = Comment.objects.get(id=comment.id)
    response = not_author_client.post(url_edit, data=FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == old_comment.text
    assert comment.news == old_comment.news
    assert comment.author == old_comment.author


def test_user_cant_delete_comment_of_another_user(
        not_author_client, comment, url_delete):
    comments_count = Comment.objects.count()
    response = not_author_client.delete(url_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_count
