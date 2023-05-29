import json
from django.test import TestCase
from django.urls import reverse

from techtest.articles.models import Article, Author
from techtest.regions.models import Region

class ArticleViewTestCase(TestCase):
    def setUp(self):
        self.article = Article.objects.create(title="Fake Article 1")
        self.region_1 = Region.objects.create(code="AL", name="Albania")
        self.region_2 = Region.objects.create(code="UK", name="United Kingdom")
        self.url = reverse("article", kwargs={"article_id": self.article.id})

    def test_serializes_single_record_with_correct_data_shape_and_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                "id": self.article.id,
                "title": "Fake Article 1",
                "content": "",
                "author": None,
                "regions": [],
            },
        )

    def test_updates_article_with_regions_and_author(self):
        author = Author.objects.create(first_name="John", last_name="Doe")
        payload = {
            "id": self.article.id,
            "title": "Updated Article",
            "content": "Lorem Ipsum",
            "author": {
                "id": author.id,
                "first_name": "Jane",
                "last_name": "Smith",
            },
            "regions": [
                {"code": "US", "name": "United States of America"},
                {"code": "AU", "name": "Austria"},
            ],
        }
        response = self.client.put(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, "Updated Article")
        self.assertEqual(self.article.content, "Lorem Ipsum")
        self.assertEqual(self.article.author, author)
        self.author.refresh_from_db()
        self.assertEqual(self.author.first_name,'John')
        self.assertEqual(self.author.last_name,'Doe')
        self.assertEqual(self.article.regions.count(), 2)
        self.assertCountEqual(
            self.article.regions.values("code", "name"),
            [
                {"code": "US", "name": "United States of America"},
                {"code": "AU", "name": "Austria"},
            ],
        )
        self.assertDictEqual(
            {
                "id": self.article.id,
                "title": "Updated Article",
                "content": "Lorem Ipsum",
                "author": {
                    "id": author.id,
                    "first_name": "Jane",
                    "last_name": "Smith",
                },
                "regions": [
                    {"code": "US", "name": "United States of America"},
                    {"code": "AU", "name": "Austria"},
                ],
            },
            response.json(),
        )

    def test_removes_article(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Article.objects.filter(pk=self.article.id).exists())

class ArticleListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("articles-list")
        self.article_1 = Article.objects.create(title="Fake Article 1")
        self.region_1 = Region.objects.create(code="AL", name="Albania")
        self.region_2 = Region.objects.create(code="UK", name="United Kingdom")
        self.article_2 = Article.objects.create(
            title="Fake Article 2", content="Lorem Ipsum"
        )
        self.article_2.regions.set([self.region_1, self.region_2])

    def test_serializes_with_correct_data_shape_and_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.json(),
            [
                {
                    "id": self.article_1.id,
                    "title": "Fake Article 1",
                    "content": "",
                    "author": None,
                    "regions": [],
                },
                {
                    "id": self.article_2.id,
                    "title": "Fake Article 2",
                    "content": "Lorem Ipsum",
                    "author": None,
                    "regions": [
                        {
                            "id": self.region_1.id,
                            "code": "AL",
                            "name": "Albania",
                        },
                        {
                            "id": self.region_2.id,
                            "code": "UK",
                            "name": "United Kingdom",
                        },
                    ],
                },
            ],
        )

    def test_creates_new_article_with_regions_and_author(self):
        author = Author.objects.create(first_name="John", last_name="Doe")
        payload = {
            "title": "Fake Article 3",
            "content": "To be or not to be",
            "author": {
                "first_name": "Jane",
                "last_name": "Smith"
            },
            "regions": [
                {"code": "US", "name": "United States of America"},
                {"code": "AU", "name": "Austria"},
            ],
        }
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        article = Article.objects.last()
        regions = Region.objects.filter(articles__id=article.id)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(article)
        self.assertEqual(regions.count(), 2)
        self.assertEqual(article.author.first_name, "Jane")
        self.assertEqual(article.author.last_name, "Smith")
        self.assertDictEqual(
            {
                "id": article.id,
                "title": "Fake Article 3",
                "content": "To be or not to be",
                "author": {
                    "id": article.author.id,
                    "first_name": "Jane",
                    "last_name": "Smith",
                },
                "regions": [
                    {
                        "id": regions.all()[0].id,
                        "code": "US",
                        "name": "United States of America",
                    },
                    {"id": regions.all()[1].id, "code": "AU", "name": "Austria"},
                ],
            },
            response.json(),
        )


class ArticleViewTestCase(TestCase):
    def setUp(self):
        self.article = Article.objects.create(title="Fake Article 1")
        self.region_1 = Region.objects.create(code="AL", name="Albania")
        self.region
