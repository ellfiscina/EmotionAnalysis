import nltk
import re
from treetagger import TreeTagger


def extend_stopwords():
    stopwords = nltk.corpus.stopwords.words('portuguese')
    words = ['é', 'quê', 'aí', 'lá', 'ia', 'aqui', 'ah', 'oh', 'ali']
    stopwords.extend(words)
    return stopwords


def tokenize(raw):
    return nltk.word_tokenize(raw.lower())


def remove_words(tokens):
    stopwords = extend_stopwords()
    return [t for t in tokens
            if t not in stopwords and t.isalpha() and len(t) > 2]


# def convert_to_text(tokens):
#     return nltk.Text(tokens)


def tags(raw):
    tagger = TreeTagger(language='portuguese')
    return tagger.tag(raw.lower())


def tags_to_token(raw):
    tagged = tags(raw)
    label = re.compile('^A|^R|^NC.P|^NCF|^V')
    tokens = []
    for tag in tagged:
        if(bool(re.search(label, tag[1])) is False or
           tag[2] == '<unknown>'):
            tokens.append(tag[0].lower())
        else:
            tokens.append(tag[2])
    return tokens


def negations(tokens):
    words = []
    for i in range(0, len(tokens)):
        if tokens[i] == 'não' and tokens[i + 1].isalpha():
            words.append(' '.join(tokens[i:i + 2]))
        elif tokens[i - 1] == 'não':
            pass
        else:
            words.append(tokens[i])
    return words
