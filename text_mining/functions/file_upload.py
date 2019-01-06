import os
import re
import PyPDF2
from text_mining.models import Book
from .pre_process import *


def UploadedFile(file, filename):
    path = 'text_mining/static/' + filename

    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    opened_file = open(path, 'rb')

    if bool(re.search(r"(\.txt)$", filename)):
        file = opened_file.read().decode('utf-8')
    elif bool(re.search(r"(\.pdf)$", filename)):
        file = readPDF(opened_file)

    book = saveBook(file, filename)
    os.remove(path)

    return book


def readPDF(file):
    reader = PyPDF2.PdfFileReader(file)
    num_pages = reader.getNumPages()
    content = ''

    for i in range(num_pages):
        content += reader.getPage(i).extractText()

    return content


def saveBook(raw, filename):
    tokens = tokenize(raw)
    tagged = tags_to_token(raw)
    book = Book(
        title=re.sub(r"\..+", "", filename),
        tokens=tokens,
        tags=tagged
    )
    book.save()
    return book
