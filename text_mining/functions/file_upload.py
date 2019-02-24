import docx
import re
import pdftotext


def UploadedFile(file, filename):
    # path = 'text_mining/static/' + filename

    # import code; code.interact(local=dict(globals(), **locals()))

    # with open(path, 'wb+') as destination:
    #     for chunk in file.chunks():
    #         destination.write(chunk)

    # opened_file = open(path, 'rb')

    if bool(re.search(r"(\.txt)$", filename)):
        opened_file = file.read().decode('utf-8')
    elif bool(re.search(r"(\.(pdf|PDF))$", filename)):
        opened_file = readPDF(file)
    elif bool(re.search(r"(\.doc(x| ))$", filename)):
        opened_file = readDOC(file)
    # os.remove(path)

    return opened_file


def readPDF(file):
    pdf = pdftotext.PDF(file)

    return "\n\n".join(pdf)


def readDOC(file):
    doc = docx.Document(file)
    content = []

    for p in doc.paragraphs:
        content.append(p.text)

    return '\n'.join(content)
