import pytest
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE
from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(client, url_home, news_list):
    assert client.get(url_home).context[
        'object_list'].count() == NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, url_home, news_list):
    all_dates = [
        news.date for news in client.get(url_home).context['object_list']]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comment_order(client, news, url_detail, comment_list):
    all_comments = client.get(url_detail).context['news'].comment_set.all()
    assert list(all_comments) == sorted(all_comments, key=lambda x: x.created)


def test_auth_user_has_form(not_author_client, url_detail):
    response = not_author_client.get(url_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_anonymous_user_has_no_form(client, url_detail):
    response = client.get(url_detail)
    assert 'form' not in response.context
