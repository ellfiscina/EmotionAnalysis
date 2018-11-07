from django.shortcuts import render
from django.http import HttpResponse

from .models import PreProcess, POSTag, Frequency, UploadedFile
from .forms import UploadFileForm

def index(request):
    return render(request, 'TextMining/index.html', {'what':'Django File Upload'})

def upload(request):
    if request.method == 'POST':
        raw = UploadedFile(request.FILES['file'], str(request.FILES['file']))

        p = PreProcess(raw)
        t = POSTag(raw)
        f = Frequency()
        f.tokens_frequency(p.filtered)

        return render(request, 'TextMining/upload.html', {'raw': raw})

    return HttpResponse("Failed")
