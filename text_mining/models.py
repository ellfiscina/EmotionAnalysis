from django.db import models
from django.contrib.postgres.fields import ArrayField


class Book(models.Model):
    title = models.CharField(max_length=100)
    tokens = ArrayField(models.CharField(max_length=100))
    # tags = ArrayField(models.CharField(max_length=100))
    sents = ArrayField(models.TextField(max_length=100))

    def __str__(self):
        return self.title


class Word(models.Model):
    word = models.CharField(max_length=50)

    def __str__(self):
        return self.word


class Emotion(models.Model):
    emotion = models.CharField(max_length=50)
    words = models.ManyToManyField(Word)

    def __str__(self):
        return self.emotion
