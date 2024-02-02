from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url',
    (
        (lf('url_edit')),
        (lf('url_delete'))
    )
)
def test_comment_edit_delete_redirect(client, url, redirect_login):
    response = client.get(url)
    assertRedirects(response, redirect_login + url)


@pytest.mark.parametrize(
    'url, parametrized_client, status',
    (
        (lf('url_detail'), lf('client'), HTTPStatus.OK),
        (lf('url_home'), lf('client'), HTTPStatus.OK),
        (lf('url_login'), lf('client'), HTTPStatus.OK),
        (lf('url_logout'), lf('client'), HTTPStatus.OK),
        (lf('url_signup'), lf('client'), HTTPStatus.OK),
        (lf('url_delete'), lf('not_author_client'), HTTPStatus.NOT_FOUND),
        (lf('url_edit'), lf('not_author_client'), HTTPStatus.NOT_FOUND),
        (lf('url_delete'), lf('author_client'), HTTPStatus.OK),
        (lf('url_edit'), lf('author_client'), HTTPStatus.OK)
    )
)
def test_avalible_for_different_pages(url, parametrized_client, status):
    response = parametrized_client.get(url)
    assert response.status_code == status
