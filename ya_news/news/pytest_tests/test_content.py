import pytest

from yanews.settings import NEWS_COUNT_ON_HOME_PAGE
from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(client, home_url, news_list):
    assert client.get(home_url).context[
        'object_list'].count() == NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, home_url, news_list):
    all_dates = [
        news.date for news in client.get(home_url).context['object_list']]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comment_order(client, news, detail_url, comment_list):
    all_comments = client.get(detail_url).context['news'].comment_set.all()
    assert list(all_comments) == sorted(all_comments, key=lambda x: x.created)


def test_auth_user_has_form(not_author_client, detail_url):
    assert isinstance(
        not_author_client.get(detail_url).context.get('form'), CommentForm)


def test_anonymous_user_has_no_form(client, detail_url):
    assert 'form' not in client.get(detail_url).context
