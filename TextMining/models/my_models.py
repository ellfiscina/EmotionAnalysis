from django.db import models
from django.contrib.postgres.fields import ArrayField


class Book(models.Model):
    class Meta:
        app_label = "TextMining"

    tokens = ArrayField(models.CharField(max_length=100))
    filtered = ArrayField(models.CharField(max_length=100))
