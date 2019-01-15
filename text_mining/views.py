from django.shortcuts import render
from .functions import UploadedFile, LexicalDiversity, MostFrequent, NewList, Emolex
from .functions.pre_process import *
from .functions.emotion_analysis import *
from .functions.context import *
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

    tokens = request.session['tokens']

    if 'list' not in request.session:
        emoList = NewList(filter_words(tokens), EMOLEX)

        request.session['list'] = emoList
    else:
        emoList = request.session['list']

    tokens_batch = batch(tokens)
    dist = generate_emotion_distribution(emoList, tokens_batch)
    tree = generate_word_count(emoList)

    return render(request,
                  'text_mining/emotion.html',
                  {'dist': dist,
                   'tree': tree})


def context(request):
    tokens = request.session['tokens']

    if 'list' not in request.session:
        emoList = NewList(filter_words(tokens), EMOLEX)
        request.session['list'] = emoList
    else:
        emoList = request.session['list']

    text = convert_to_text(tokens)
    dist = FreqDist(filter_words(tokens))
    ngrams = n_grams(text, emoList)
    similar_tokens = similar(text, emoList)
    context = concordance(text, dist)
    return render(request,
                  'text_mining/context.html',
                  {'ngrams': ngrams,
                   'tokens': similar_tokens,
                   'context': context})
