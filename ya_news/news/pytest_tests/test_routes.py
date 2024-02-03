from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

author_client = lazy_fixture('author_client')
not_author_client = lazy_fixture('not_author_client')
client = lazy_fixture('client')

home_url = lazy_fixture('home_url')
login_url = lazy_fixture('login_url')
logout_url = lazy_fixture('logout_url')
signup_url = lazy_fixture('signup_url')
detaul_url = lazy_fixture('detail_url')
edit_url = lazy_fixture('edit_url')
delete_url = lazy_fixture('delete_url')

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, redirect',
    (
        (edit_url, lazy_fixture('redirect_edit')),
        (delete_url, lazy_fixture('redirect_delete'))
    )
)
def test_comment_edit_delete_redirect(client, url, redirect):
    assertRedirects(client.get(url), redirect)


@pytest.mark.parametrize(
    'url, parametrized_client, status',
    (
        (detaul_url, client, HTTPStatus.OK),
        (home_url, client, HTTPStatus.OK),
        (login_url, client, HTTPStatus.OK),
        (logout_url, client, HTTPStatus.OK),
        (signup_url, client, HTTPStatus.OK),
        (delete_url, not_author_client, HTTPStatus.NOT_FOUND),
        (edit_url, not_author_client, HTTPStatus.NOT_FOUND),
        (delete_url, author_client, HTTPStatus.OK),
        (edit_url, author_client, HTTPStatus.OK)
    )
)
def test_avalible_for_different_pages(url, parametrized_client, status):
    assert parametrized_client.get(url).status_code == status
