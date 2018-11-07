from django.shortcuts import render
from django.http import HttpResponse

from .models import PreProcess, POSTag, Frequency, handle_uploaded_file
from .forms import UploadFileForm

def index(request):
    # file = open('../TextMining/books/senhora.txt', 'r', encoding="utf8")
    # raw = file.read()
    # p = PreProcess(raw)
    # t = POSTag(raw)
    # f = Frequency()
    # f.tokens_frequency(p.filtered)

    # context = {
    #     'raw': raw,
    #     'p': p,
    #     'f': f,
    #     'm': f.most_frequent(p.filtered, 20)
    # }
    # return render(request, 'TextMining/index.html', context)

    return render(request, 'TextMining/index.html', {'what':'Django File Upload'})

def upload(request):
    if request.method == 'POST':
        raw = handle_uploaded_file(request.FILES['file'], str(request.FILES['file']))
        return render(request, 'TextMining/upload.html', {'raw': raw})

    return HttpResponse("Failed")


