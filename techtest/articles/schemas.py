from marshmallow import validate
from marshmallow import fields
from marshmallow import Schema
from marshmallow.decorators import post_load

from techtest.articles.models import Article, Author
from techtest.regions.models import Region
from techtest.regions.schemas import RegionSchema

class AuthorSchema(Schema):
    id = fields.Integer()
    first_name = fields.String(validate=validate.Length(max=255))
    last_name = fields.String(validate=validate.Length(max=255))

class ArticleSchema(Schema):
    id = fields.Integer()
    title = fields.String(validate=validate.Length(max=255))
    content = fields.String()
    author = fields.Nested(AuthorSchema, required=False)

    regions = fields.Method(
        required=False, serialize="get_regions", deserialize="load_regions"
    )

    def get_regions(self, article):
        return RegionSchema().dump(article.regions.all(), many=True)

    def load_regions(self, regions):
        return [Region.objects.get_or_create(id=region.pop("id", None), defaults=region)[0] for region in regions]

    @post_load
    def update_or_create(self, data, *args, **kwargs):
        regions = data.pop("regions", None)
        author_data = data.pop('author', None)
        author = None
        if author_data:
            author, _ = Author.objects.update_or_create(id=author_data.get('id', None),first_name= author_data.get("first_name", self.author.first_name),last_name= author_data.get("last_name", self.author.last_name), defaults=author_data)
        article, _ = Article.objects.update_or_create(id=data.pop("id", None), defaults=data)
        if isinstance(regions, list):
            article.regions.set(regions)
        if author:
            article.author = author
            article.save()

        return article
