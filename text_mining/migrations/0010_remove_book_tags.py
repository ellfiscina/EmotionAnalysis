# Generated by Django 2.1.5 on 2019-01-12 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('text_mining', '0009_book_sents'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='tags',
        ),
    ]