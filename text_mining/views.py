from django.shortcuts import render
from .functions import UploadedFile, LexicalDiversity, MostFrequent
from .functions.pre_process import *
from .functions.emotion_analysis import *
from .models import Book
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

    # import code; code.interact(local=dict(globals(), **locals()))
    frequent = MostFrequent(filtered, 150)
    commonArray = most_common_array(newList(filtered))

    diversity = {
        'qtd_tokens': len(tokens),
        'qtd_filtered': len(filtered),
        'qtd_uniq_tokens': len(set(tokens)),
        'qtd_uniq_filtered': len(set(filtered)),
        'lexical': LexicalDiversity(filtered)
    }

    return render(request,
                  'text_mining/word.html',
                  {'diversity': diversity,
                   'tokens': json.dumps(tokens),
                   'commonArray': json.dumps(commonArray),
                   'frequent': frequent
                   })


def emotion(request):
    book_id = request.session['book_id']
    tokens = remove_words(Book.objects.get(id=book_id).tokens)
    emotion = generate_word_count(newList(tokens))
    return render(request, 'text_mining/emotion.html', {'emotion': emotion})
