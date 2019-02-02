from django.shortcuts import render
from .functions import UploadedFile, LexicalDiversity, MostFrequent, NewList, Emolex
from .functions.pre_process import *
from .functions.emotion_analysis import *
from .functions.context import *
from nltk import FreqDist
from nltk.text import ConcordanceIndex
import json

EMOLEX = Emolex()


def index(request):
    return render(request, 'text_mining/index.html')


def word(request):
    if request.method == 'POST':
        for key in list(request.session.keys()):
            del request.session[key]

        raw = UploadedFile(request.FILES['file'], str(request.FILES['file']))
        request.session['raw'] = raw
    else:
        raw = request.session['raw']

    tokens = tokenize(raw)
    tagged = tags_to_token(raw)
    filtered = filter_words(tagged)

    # import code; code.interact(local=dict(globals(), **locals()))
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
        'tokens': json.dumps(tagged),
        'commonArray': json.dumps(commonArray),
        'frequent': frequent
    }

    return render(request, 'text_mining/word.html', context)


def emotion(request):

    tagged = tags_to_token(request.session['raw'])

    if 'list' not in request.session:
        emoList = NewList(filter_words(tagged), EMOLEX)

        request.session['list'] = emoList
    else:
        emoList = request.session['list']

    tokens_batch = batch(tagged)
    dist = generate_emotion_distribution(emoList, tokens_batch)
    tree = generate_word_count(emoList)

    return render(request,
                  'text_mining/emotion.html',
                  {'dist': dist,
                   'tree': tree})


def context(request):
    tokens = tokenize(request.session['raw'])

    if 'list' not in request.session:
        emoList = NewList(filter_words(tokens), EMOLEX)
        request.session['list'] = emoList
    else:
        emoList = request.session['list']

    text = convert_to_text(tokens)
    filtered = filter_words(tokens)
    max_token = max_dist(emoList)
    ngrams = n_grams(text, max_token, 5)
    colls = collocations(filtered)
    context = concordance(ConcordanceIndex(tokens), max_token)
    tree = treeword(text, FreqDist(filtered).max(), max_token)

    return render(request,
                  'text_mining/context.html',
                  {'max': max_token,
                   'ngrams': ngrams[:10],
                   'collocations': colls,
                   'context': context,
                   'treeword': tree})
