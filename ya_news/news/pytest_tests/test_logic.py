import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError
from http import HTTPStatus

from news.models import Comment
from news.forms import BAD_WORDS, WARNING

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_note(client, form_data, news_id):
    url = reverse('news:detail', args=news_id)
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_autorized_user_can_create_comment(
    author_client, author, form_data, news, news_id
):
    url = reverse('news:detail', args=news_id)
    response = author_client.post(url, data=form_data)
    expected_url = f'{url}#comments'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author
    assert new_comment.news == news


@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_user_cant_use_bad_words(author_client, bad_word, news_id):
    bad_words_data = {'text': f'Текст {bad_word} текст'}
    url = reverse('news:detail', args=news_id)
    response = author_client.post(url, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
        author_client, news_id, comment, comment_id, form_data
):
    url = reverse('news:edit', args=comment_id)
    response = author_client.post(url, data=form_data)
    news_url = reverse('news:detail', args=news_id)
    url_to_comments = f'{news_url}#comments'
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_author_can_delete_comment(author_client, news_id, comment_id):
    url = reverse('news:delete', args=comment_id)
    response = author_client.delete(url)
    news_url = reverse('news:detail', args=news_id)
    url_to_comments = f'{news_url}#comments'
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == 0


def test_user_cant_edit_comment_of_another_user(
        not_author_client, comment, comment_id, form_data
):
    url = reverse('news:edit', args=comment_id)
    old_comment_text = comment.text
    response = not_author_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == old_comment_text


def test_user_cant_delete_comment_of_another_user(
        not_author_client, news_id, comment_id
):
    url = reverse('news:delete', args=comment_id)
    response = not_author_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
