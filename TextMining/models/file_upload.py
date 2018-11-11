import os


def UploadedFile(file, filename):
    media_path = 'media/TextMining/'
    if not os.path.exists(media_path):
        os.mkdir(media_path)

    with open(media_path + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    file = open(media_path + filename, 'r', encoding="utf8")
    return file.read()
