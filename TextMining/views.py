from django.shortcuts import render
from django.http import HttpResponse
from .models import PreProcess, POSTag, Frequency, UploadedFile, Analysis
import json
import matplotlib.pyplot as plt, mpld3

def index(request):
    return render(request, 'TextMining/index.html')

def upload(request):
    if request.method == 'POST':
        raw = UploadedFile(request.FILES['file'], str(request.FILES['file']))
        p = PreProcess(raw)
        t = POSTag(raw)
        f = Frequency(p.filtered)
        a = Analysis(t.filtered)
        d = p.text.dispersion_plot(a.commonArray)

        return render(request, 'TextMining/upload.html',
                      {'simple': p.to_dict(),
                       'tagged': json.dumps(t.to_dict()),
                       'frequency': f.to_dict(),
                       'emotion': json.dumps(a.to_dict()),
                       'dispersion': d})

    return HttpResponse("Failed")
