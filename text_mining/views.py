from django.shortcuts import render
from .functions import UploadedFile, LexicalDiversity, MostFrequent, NewList, Emolex
from .functions.pre_process import *
from .functions.emotion_analysis import *
from nltk import FreqDist
import json

EMOLEX = Emolex()


def index(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, 'text_mining/index.html')


def word(request):
    if request.method == 'POST':
        for key in list(request.session.keys()):
            del request.session[key]

        tokens = UploadedFile(
            request.FILES['file'], str(request.FILES['file']))
        request.session['tokens'] = tokens
    else:
        tokens = request.session['tokens']

    filtered = filter_words(tokens)

    commonArray = MostFrequent(filtered, 5)
    commonWords = MostFrequent(filtered, 150)

    dist = FreqDist(filtered)
    frequent = [{"text": token, "value": dist[token]} for token in commonWords]

    diversity = {
        'qtd_tokens': len(tokens),
        'qtd_filtered': len(filtered),
        'qtd_uniq_tokens': len(set(tokens)),
        'qtd_uniq_filtered': len(set(filtered)),
        'lexical': LexicalDiversity(filtered)
    }

    context = {
        'diversity': diversity,
        'tokens': json.dumps(tokens),
        'commonArray': json.dumps(commonArray),
        'frequent': frequent
    }

    return render(request, 'text_mining/word.html', context)


def emotion(request):

    if 'dist' not in request.session:
        tokens = request.session['tokens']
        tokens_batch = batch(tokens)

        emoList = NewList(filter_words(tokens), EMOLEX)

        dist = generate_emotion_distribution(emoList, tokens_batch)
        tree = generate_word_count(emoList)
        request.session['dist'] = dist
        request.session['tree'] = tree
    else:
        dist = request.session['dist']
        tree = request.session['tree']

    return render(request,
                  'text_mining/emotion.html',
                  {'dist': dist,
                   'tree': tree})
