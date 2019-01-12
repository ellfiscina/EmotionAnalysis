from django.shortcuts import render
from .functions import UploadedFile, LexicalDiversity, MostFrequent
from .functions.pre_process import *
from .functions.emotion_analysis import *
from .models import Book
from nltk import FreqDist
import json
import django_rq
import time

queue = django_rq.get_queue('high', is_async=True, default_timeout=360)


def index(request):
    return render(request, 'text_mining/index.html')


def word(request):
    if request.method == 'POST':
        for key in list(request.session.keys()):
            del request.session[key]
        book = UploadedFile(request.FILES['file'], str(request.FILES['file']))
        request.session['book_id'] = book.id
    else:
        book_id = request.session['book_id']
        book = Book.objects.get(id=book_id)

    tokens = book.tokens
    filtered = remove_words(tokens)

    job = queue.enqueue(newList, filtered)
    request.session['job_id'] = job.id
    # import code; code.interact(local=dict(globals(), **locals()))
    # tags = book.tags
    # filtered_tags = remove_words(tags)

    # emoList = newList(filtered)
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
        job = queue.fetch_job(request.session['job_id'])
        # import code; code.interact(local=dict(globals(), **locals()))
        book_id = request.session['book_id']
        book = Book.objects.get(id=book_id)
        sents = join_sentences(tokenize_sentence(book.sents))
        # tokens = remove_words(book.tokens)
        emoList = job.result
        job.delete()

        dist = generate_emotion_distribution(emoList, sents)
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
