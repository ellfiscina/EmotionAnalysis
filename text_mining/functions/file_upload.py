import os
import re
import PyPDF2
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

    tokens = tokenize(file)
    os.remove(path)

    return tokens


def readPDF(file):
    reader = PyPDF2.PdfFileReader(file)
    num_pages = reader.getNumPages()
    content = ''

    for i in range(num_pages):
        content += reader.getPage(i).extractText()

    return content
