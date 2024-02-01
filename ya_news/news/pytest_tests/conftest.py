from datetime import datetime, timedelta

import pytest
from django.test.client import Client
from django.utils import timezone

from news.models import Comment, News
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст'
    )


@pytest.fixture
def news_list():
    return News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Текст',
            date=datetime.today() - timedelta(days=index)
        )
        for index in range(NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def news_id(news):
    return news.id,


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Комментарий'
    )


@pytest.fixture
def comment_list(news, author):
    for index in range(2):
        comment = Comment.objects.create(
            author=author,
            news=news,
            text=f'Комментарий {index}',
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()


@pytest.fixture
def comment_id(comment):
    return comment.id,


@pytest.fixture
def form_data():
    return {'text': 'Комментарий'}
