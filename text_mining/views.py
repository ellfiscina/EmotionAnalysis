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
        book = UploadedFile(request.FILES['file'], str(request.FILES['file']))
        request.session['book_id'] = book.id
    else:
        book_id = request.session['book_id']
        book = Book.objects.get(id=book_id)

    tokens = book.tokens
    filtered = remove_words(tokens)

    tags = book.tags
    filtered_tags = remove_words(tags)

    emoList = newList(filtered_tags)
    # import code; code.interact(local=dict(globals(), **locals()))
    commonArray = MostFrequent(emoList, 5)
    commonWords = MostFrequent(emoList, 150)

    dist = FreqDist(filtered_tags)
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
    sents = tokenize_sentence(book.sents)

    if 'dist' not in request.session:
        dist = generate_emotion_distribution(newList(book.tags), sents)
        request.session['dist'] = dist
    else:
        dist = request.session['dist']

    # import code; code.interact(local=dict(globals(), **locals()))
    return render(request,
                  'text_mining/emotion.html',
                  {'dist': dist})


def treemap(request):
    book_id = request.session['book_id']
    tokens = remove_words(Book.objects.get(id=book_id).tags)
    if 'tree' not in request.session:
        tree = generate_word_count(newList(tokens))
        request.session['tree'] = tree
    else:
        tree = request.session['tree']

    return render(request, 'text_mining/treemap.html', {'tree': tree})
