from django.shortcuts import render
from .functions import UploadedFile, LexicalDiversity, MostFrequent
from .functions.pre_process import *
from .functions.emotion_analysis import *
from .models import Book
from nltk import FreqDist
import json


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

    # tags = book.tags
    # filtered_tags = remove_words(tags)

    # emoList = newList(filtered)
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
        'tokens': json.dumps(tokens),
        'commonArray': json.dumps(commonArray),
        'frequent': frequent
    }

    return render(request, 'text_mining/word.html', context)


def emotion(request):
    book_id = request.session['book_id']
    book = Book.objects.get(id=book_id)
    sents = join_sentences(tokenize_sentence(book.sents))
    tokens = remove_words(book.tokens)

    if 'dist' not in request.session:
        dist = generate_emotion_distribution(newList(tokens), sents)
        tree = generate_word_count(newList(tokens))
        request.session['dist'] = dist
        request.session['tree'] = tree
    else:
        dist = request.session['dist']
        tree = request.session['tree']

    # import code; code.interact(local=dict(globals(), **locals()))
    return render(request,
                  'text_mining/emotion.html',
                  {'dist': dist,
                   'tree': tree})
