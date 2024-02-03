from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

pytestmark = pytest.mark.django_db
url_client_status = (
    (lazy_fixture('detail_url'),
     lazy_fixture('client'),
     HTTPStatus.OK),
    (lazy_fixture('home_url'),
     lazy_fixture('client'),
     HTTPStatus.OK),
    (lazy_fixture('login_url'),
     lazy_fixture('client'),
     HTTPStatus.OK),
    (lazy_fixture('logout_url'),
     lazy_fixture('client'),
     HTTPStatus.OK),
    (lazy_fixture('signup_url'),
     lazy_fixture('client'),
     HTTPStatus.OK),
    (lazy_fixture('delete_url'),
     lazy_fixture('not_author_client'),
     HTTPStatus.NOT_FOUND),
    (lazy_fixture('edit_url'),
     lazy_fixture('not_author_client'),
     HTTPStatus.NOT_FOUND),
    (lazy_fixture('delete_url'),
     lazy_fixture('author_client'),
     HTTPStatus.OK),
    (lazy_fixture('edit_url'),
     lazy_fixture('author_client'),
     HTTPStatus.OK)
)


@pytest.mark.parametrize(
    'url',
    (
        (lazy_fixture('edit_url')),
        (lazy_fixture('delete_url'))
    )
)
def test_comment_edit_delete_redirect(client, url, redirect_url):
    assertRedirects(client.get(url), redirect_url(url))


@pytest.mark.parametrize(
    'url, parametrized_client, status',
    url_client_status
)
def test_avalible_for_different_pages(url, parametrized_client, status):
    assert parametrized_client.get(url).status_code == status
