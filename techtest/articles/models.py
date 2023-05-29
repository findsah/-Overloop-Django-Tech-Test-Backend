from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    
class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.SET_NULL)

    regions = models.ManyToManyField(
        'regions.Region', related_name='articles', blank=True
    )

