# Generated by Django 2.1.3 on 2019-01-06 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('text_mining', '0002_emotion'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Emotion',
        ),
    ]
