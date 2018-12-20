from django.shortcuts import render
from django.http import HttpResponse
from .models import PreProcess, POSTag, Frequency, UploadedFile, Analysis, LexicalDispersion
import json
import six

def index(request):
    return render(request, 'TextMining/index.html')

def word(request):
    if request.method == 'POST':
        raw = UploadedFile(request.FILES['file'], str(request.FILES['file']))
        p = PreProcess(raw)
        t = POSTag(raw)
        f = Frequency(p.filtered)
        a = Analysis(t.filtered)

        l = LexicalDispersion()

        request.session['emotion'] = a.wordCounts

        myFiles = []

        for w in a.commonArray:
          fig = l.plot_dis(p.tokens, w)
          tmp = six.StringIO()
          fig.savefig(tmp, format='svg', bbox_inches='tight')
          myFiles.append(tmp.getvalue())
        
        return render(request, 'TextMining/word.html',
                      {'simple': p.to_dict(),
                       'frequency': f.to_dict(),
                       'img1': myFiles[0],
                       'img2': myFiles[1],
                       'img3': myFiles[2],
                       'img4': myFiles[3],
                       'img5': myFiles[4]
                       })

    return HttpResponse("Failed")

def emotion(request):
  emotion = request.session['emotion']
  return render(request, 'TextMining/emotion.html', {'emotion': emotion})