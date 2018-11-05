from django.shortcuts import render
import nltk

def index(request):
  file = open('../TextMining/books/senhora.txt', 'r', encoding="utf8")
  raw = file.read()
  tokens = nltk.word_tokenize(raw.lower())
  return render(request, 'textmining/index.html', {'raw': raw,
                                                   'tokens': tokens})
