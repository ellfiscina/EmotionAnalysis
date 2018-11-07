import os


def UploadedFile(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')

    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    file = open('upload/' + filename, 'r', encoding="utf8")
    return file.read
