import os
import re
from text_mining.models import Book
from .pre_process import *


def UploadedFile(file, filename):
    media_path = 'text_mining/static/'
    if not os.path.exists(media_path):
        os.mkdir(media_path)

    with open(media_path + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    file = open(media_path + filename, 'r', encoding="utf8")
    book = saveBook(file.read(), filename)
    os.remove(media_path + filename)

    return book


def saveBook(raw, filename):
    tokens = tokenize(raw)
    tagged = tags(raw)
    book = Book(
        title=re.sub(r"\..+", "", filename),
        tokens=tokens,
        tags=tagged
    )
    book.save()
    return book
