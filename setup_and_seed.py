import django
import os
import sys
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techtest.settings")
sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), "..", ".."))
django.setup()

from techtest.articles.models import Article, Author
from techtest.regions.models import Region
from django.core import management

# Migrate
management.call_command("migrate", no_input=True)
# Seed
author_1 = Author.objects.create(first_name="John", last_name="Doe")
author_2 = Author.objects.create(first_name="Jane", last_name="Smith")

# Create regions if they don't exist
region_al, _ = Region.objects.get_or_create(code="AL", name="Albania")
region_uk, _ = Region.objects.get_or_create(code="UK", name="United Kingdom")
region_au, _ = Region.objects.get_or_create(code="AU", name="Austria")
region_us, _ = Region.objects.get_or_create(code="US", name="United States of America")

Article.objects.create(title="Fake Article", content="Fake Content", author=author_1).regions.set(
    [region_al, region_uk]
)
Article.objects.create(title="Fake Article", content="Fake Content")
Article.objects.create(title="Fake Article", content="Fake Content")
Article.objects.create(title="Fake Article", content="Fake Content")
Article.objects.create(title="Fake Article", content="Fake Content", author=author_2).regions.set(
    [region_au, region_us]
)
