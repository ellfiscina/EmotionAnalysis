from django.shortcuts import render
from .functions import UploadedFile, LexicalDiversity, MostFrequent, NewList
from .functions.pre_process import *
from .functions.emotion_analysis import *
from .functions.context import *
from nltk import FreqDist
from nltk.text import ConcordanceIndex
import json
import django_rq
import random


queue = django_rq.get_queue('default', is_async=True, result_ttl=-1)


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

    if 'jid' not in request.session:
        job = queue.enqueue(NewList, filter_words(negations(tagged)))
        request.session['jid'] = job.id

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
        'frequent': frequent,
        'filtered': json.dumps(filtered),
    }

    return render(request, 'text_mining/word.html', context)


def emotion(request):
    if 'list' not in request.session:
        job = queue.fetch_job(request.session['jid'])
        # emoList = NewList(filter_words(negations(tagged)), EMOLEX)

        tagged = tags_to_token(request.session['raw'])
        tokens_batch = batch(tagged)
        emoList = job.result
        job.delete()
        dist = generate_emotion_distribution(emoList, tokens_batch)
        tree = generate_word_count(emoList)
        request.session['list'] = emoList
        request.session['dist'] = dist
        request.session['tree'] = tree
    else:
        emoList = request.session['list']
        dist = request.session['dist']
        tree = request.session['tree']

    return render(request,
                  'text_mining/emotion.html',
                  {'dist': dist,
                   'tree': tree})


def context(request):
    error = False
    tokens = tokenize(request.session['raw'])

    if 'list' not in request.session:
        job = queue.fetch_job(request.session['jid'])
        # tagged = tags_to_token(request.session['raw'])
        # emoList = NewList(filter_words(negations(tagged)), EMOLEX)
        emoList = job.result
        job.delete()
        request.session['list'] = emoList
    else:
        emoList = request.session['list']

    text = convert_to_text(tokens)
    filtered = filter_words(tokens)
    max_token = max_dist(emoList)
    ngrams = n_grams(text, max_token, 5)
    colls = collocations(filtered)
    context = concordance(ConcordanceIndex(tokens), max_token)

    if request.method == 'POST':
        tree = getDict(text, request.POST['word'])
        if not tree['name']:
            error = True
    else:
        tree = getDict(text, max_token)

    return render(request,
                  'text_mining/context.html',
                  {'max': max_token,
                   'ngrams': random.sample(ngrams, 10),
                   'collocations': colls,
                   'context': context,
                   'treeword': tree,
                   'error': error})
