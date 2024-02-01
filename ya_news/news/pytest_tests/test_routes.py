from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:detail', pytest.lazy_fixture('news_id')),
        ('news:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None)
    )
)
@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
    )
)
@pytest.mark.parametrize(
    'name',
    (
        ('news:delete'),
        ('news:edit'),
    )
)
def test_availability_for_comment_edit_and_delete(
    parametrized_client, expected_status, name, comment_id,
):
    url = reverse(name, args=comment_id)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:delete', pytest.lazy_fixture('comment_id')),
        ('news:edit', pytest.lazy_fixture('comment_id')),
    )
)
@pytest.mark.django_db
def test_redirect(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
