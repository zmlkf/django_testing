import pytest
from django.urls import reverse
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE
from news.forms import CommentForm

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures('news_list')
def test_news_count(client):
    url = reverse('news:home')
    response = client.get(url)
    news_count = response.context['object_list'].count()
    assert news_count == NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.usefixtures('news_list')
def test_news_order(client):
    url = reverse('news:home')
    response = client.get(url)
    all_dates = [news.date for news in response.context['object_list']]
    assert all_dates == sorted(all_dates, reverse=True)


@pytest.mark.usefixtures('comment_list')
def test_comment_order(client, news_id):
    url = reverse('news:detail', args=news_id)
    response = client.get(url)
    news = response.context['news']
    all_comments = list(news.comment_set.all())
    assert all_comments == sorted(all_comments, key=lambda x: x.created)


@pytest.mark.parametrize(
    'user, comment_form',
    (
        (pytest.lazy_fixture('not_author_client'), True),
        (pytest.lazy_fixture('client'), False),
    )
)
def test_client_has_form(user, comment_form, news_id):
    url = reverse('news:detail', args=news_id)
    response = user.get(url)
    assert ('form' in response.context) == comment_form
    if comment_form:
        assert isinstance(response.context['form'], CommentForm)
