from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=50)

    def __str__(self):
        return self.word


class Emotion(models.Model):
    emotion = models.CharField(max_length=50)
    words = models.ManyToManyField(Word)

    def __str__(self):
        return self.emotion
