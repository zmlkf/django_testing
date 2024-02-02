from http import HTTPStatus

from django.contrib.auth import get_user_model

from .basecase import BaseCase
from .constants_urls import (URL_ADD_NOTE, URL_DELETE, URL_DETAIL,
                             URL_EDIT_NOTE, URL_HOME, URL_LOGIN, URL_LOGOUT,
                             URL_NOTES_LIST, URL_SIGNUP, URL_SUCCESS)

User = get_user_model()


class TestRoutes(BaseCase):

    def test_pages_availability(self):
        urls_users_statuses = (
            (URL_LOGIN, self.client, HTTPStatus.OK),
            (URL_LOGOUT, self.client, HTTPStatus.OK),
            (URL_SIGNUP, self.client, HTTPStatus.OK),
            (URL_HOME, self.client, HTTPStatus.OK),
            (URL_ADD_NOTE, self.author_client, HTTPStatus.OK),
            (URL_NOTES_LIST, self.author_client, HTTPStatus.OK),
            (URL_SUCCESS, self.author_client, HTTPStatus.OK),
            (URL_EDIT_NOTE, self.author_client, HTTPStatus.OK),
            (URL_DELETE, self.author_client, HTTPStatus.OK),
            (URL_DETAIL, self.author_client, HTTPStatus.OK),
            (URL_EDIT_NOTE, self.other_author_client, HTTPStatus.NOT_FOUND),
            (URL_DELETE, self.other_author_client, HTTPStatus.NOT_FOUND),
            (URL_DETAIL, self.other_author_client, HTTPStatus.NOT_FOUND),
        )
        for url, user, status in urls_users_statuses:
            with self.subTest(url=url, user=user, status=status):
                self.assertEqual(user.get(url).status_code, status)

    def test_redirect_for_anonymous_client(self):
        urls = (URL_ADD_NOTE, URL_NOTES_LIST, URL_SUCCESS,
                URL_EDIT_NOTE, URL_DELETE, URL_DETAIL)
        for url in urls:
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url), f'{URL_LOGIN}?next={url}')
