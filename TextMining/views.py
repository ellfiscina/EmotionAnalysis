from django.shortcuts import render
from django.http import HttpResponse
from .models import PreProcess, POSTag, Frequency, UploadedFile, Analysis
import json


def index(request):
    return render(request, 'TextMining/index.html')


def word(request):
    if request.method == 'POST':
        raw = UploadedFile(request.FILES['file'], str(request.FILES['file']))
        p = PreProcess(raw)
        t = POSTag(raw)
        f = Frequency(p.filtered)
        a = Analysis(t.filtered)

        request.session['emotion'] = a.wordCounts

        return render(request, 'TextMining/word.html',
                      {'simple': p.to_dict(),
                       'diversity': f.lexical_diversity(),
                       'tokens': json.dumps(p.tokens),
                       'commonArray': json.dumps(a.commonArray),
                       'frequent': f.most_frequent(150)
                       })

    return HttpResponse("Failed")


def emotion(request):
    emotion = request.session['emotion']
    return render(request, 'TextMining/emotion.html', {'emotion': emotion})
