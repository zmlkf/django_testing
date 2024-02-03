from datetime import datetime, timedelta

import pytest
from django.test.client import Client
from django.urls import reverse
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
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Текст',
            date=datetime.today() - timedelta(days=index)
        )
        for index in range(NEWS_COUNT_ON_HOME_PAGE + 1)
    )


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
    for index in range(222):
        comment = Comment.objects.create(
            author=author,
            news=news,
            text=f'Комментарий {index}',
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def redirect_detail(login_url, detail_url):
    return f'{login_url}?next={detail_url}'


@pytest.fixture
def redirect_edit(login_url, edit_url):
    return f'{login_url}?next={edit_url}'


@pytest.fixture
def redirect_delete(login_url, delete_url):
    return f'{login_url}?next={delete_url}'
