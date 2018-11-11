from django.shortcuts import render
from django.http import HttpResponse
from .models import PreProcess, POSTag, Frequency, UploadedFile, Analysis


def index(request):
    return render(request, 'TextMining/index.html')


def upload(request):
    if request.method == 'POST':
        raw = UploadedFile(request.FILES['file'], str(request.FILES['file']))
        p = PreProcess(raw)
        t = POSTag(raw)
        f = Frequency(p.filtered)
        a = Analysis(t.filtered)

        token_analysis = {
            'tokens': p.tokens,
            'filtered': p.filtered,
            'text': p.text,
            'diversity': f.lexical_diversity(),
            'frequent': f.most_frequent(20)
        }

        emotion_analysis = {
            'emotions': a.emotionCounts,
            'words': a.wordCounts
        }

        return render(request, 'TextMining/upload.html',
                      {'info': token_analysis,
                       'emotion': emotion_analysis})

    return HttpResponse("Failed")
