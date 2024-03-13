from django.db import models
from django.db.models.functions import Now, Length


# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=64)
    body = models.TextField()
    published = models.BooleanField(db_default=True)
    created = models.DateTimeField(db_default=Now())
    character_count = models.GeneratedField(
        expression=Length('body'),
        output_field=models.IntegerField(),
        db_persist=True
    )
