from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from news.models import News

User = get_user_model()


class TestCheck(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        News.objects.bulk_create([News(
            title=f'news_{i}',
            text=f'text_{i}',
        ) for i in range(12)])

    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse('news:home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_with_subtests(self):
        news = News.objects.all()
        for news_post in news:
            with self.subTest(news_post):
                print(news_post)
                response = self.client.get(
                    reverse('news:detail', kwargs={'pk': news_post.id})
                )
                self.assertEqual(response.status_code, HTTPStatus.OK, 'Не ОК')
