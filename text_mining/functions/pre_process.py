import nltk
import re
from treetagger import TreeTagger


def extend_stopwords():
    stopwords = nltk.corpus.stopwords.words('portuguese')
    words = ['ali', 'agora', 'ainda', 'alguém', 'algum', 'alguma', 'alguns',
             'algumas', 'ante', 'antes', 'após', 'através', 'cada', 'coisa',
             'contra', 'contudo', 'daquele', 'daqueles', 'dessa', 'dessas',
             'desse', 'desses', 'desta', 'destas', 'deste', 'deste', 'destes',
             'dever', 'dizer', 'ser', 'enquanto', 'fazer', 'grande', 'la',
             'lá', 'lo', 'mesma', 'mesmas', 'mesmos', 'muita', 'muitas',
             'muitos', 'nenhum', 'nessa', 'nessas', 'nesta', 'nestas',
             'ninguém', 'nunca', 'outra', 'outras', 'outro', 'outros',
             'pequeno', 'per', 'perante', 'poder', 'pois', 'porém', 'porque',
             'posso', 'pouco', 'poucos', 'primeiro', 'própria', 'ir',
             'próprio', 'qual', 'quanto', 'ser', 'quantos', 'sempre', 'si',
             'sob', 'sobre', 'talvez', 'tampouco', 'ter', 'ti', 'tido', 'toda',
             'todas', 'todavia', 'todo', 'todos', 'tudo', 'último', 'umas',
             'uns', 'vendo', 'ver', 'vez', 'vindo', 'vir', 'vós', 'haver']

    stopwords.extend(words)
    return stopwords


def tokenize(raw):
    return nltk.word_tokenize(raw.lower())


def remove_words(tokens):
    stopwords = extend_stopwords()
    return [t for t in tokens if t not in stopwords and t.isalpha() and len(t) > 2]


# def convert_to_text(tokens):
#     return nltk.Text(tokens)

def sentences(raw):
    return nltk.sent_tokenize(raw.lower())


def tokenize_sentence(sents):
    return [tokenize(s) for s in sents]


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


# def negations(tokens):
#     words = []
#     for i in range(0, len(tokens)):
#         if tokens[i] == 'não' and tokens[i + 1].isalpha():
#             words.append(' '.join(tokens[i:i + 2]))
#         elif tokens[i - 1] == 'não':
#             pass
#         else:
#             words.append(tokens[i])
#     return words
