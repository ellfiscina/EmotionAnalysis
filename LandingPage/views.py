from django.shortcuts import render
from .models import PreProcess, POSTag, Frequency


def index(request):
    file = open('../TextMining/books/senhora.txt', 'r', encoding="utf8")
    raw = file.read()
    p = PreProcess(raw)
    t = POSTag(raw)
    f = Frequency()
    f.tokens_frequency(p.filtered)

    context = {
        'raw': raw,
        'p': p,
        'f': f,
        'm': f.most_frequent(p.filtered, 20)
    }
    return render(request, 'LandingPage/index.html', context)
