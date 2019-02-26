import nltk
import math
import re
import string
from treetagger import TreeTagger


# converte o texto em uma lista de tokens
def tokenize(raw):
    return nltk.word_tokenize(raw.lower())


# salva a lista de stopwords do corpus do nltk e acrescenta outras palavras
def extend_stopwords():
    stopwords = nltk.corpus.stopwords.words('portuguese')
    words = ['ali', 'agora', 'ainda', 'alguém', 'algum', 'alguma', 'alguns',
             'algumas', 'ante', 'antes', 'após', 'através', 'cada', 'coisa',
             'contra', 'contudo', 'daquele', 'daqueles', 'dessa', 'dessas',
             'desse', 'desses', 'desta', 'destas', 'deste', 'deste', 'destes',
             'dever', 'dizer', 'enquanto', 'estar', 'fazer', 'grande', 'la',
             'lá', 'lo', 'mesma', 'mesmas', 'mesmos', 'muita', 'muitas', 'aí',
             'muitos', 'nenhum', 'nessa', 'nessas', 'nesta', 'nestas', 'ah',
             'ninguém', 'nunca', 'outra', 'outras', 'outro', 'outros', 'oh',
             'pequeno', 'per', 'perante', 'poder', 'pois', 'porém', 'porque',
             'posso', 'pouco', 'poucos', 'primeiro', 'própria', 'ir', 'cap.',
             'próprio', 'qual', 'quanto', 'ser', 'quantos', 'sempre', 'si',
             'sob', 'sobre', 'talvez', 'tampouco', 'ter', 'ti', 'tido', 'toda',
             'todas', 'todavia', 'todo', 'todos', 'tudo', 'último', 'umas',
             'uns', 'vendo', 'ver', 'vez', 'vindo', 'vir', 'vós', 'haver',
             'capítulo', '...', 'd.']

    stopwords.extend(words)
    return stopwords


def remove_stopwords(tokens):
    stopwords = extend_stopwords()
    return [t for t in tokens if t not in stopwords]


def remove_pontuaction(tokens):
    return [t for t in tokens if t not in string.punctuation]


def remove_one_letter(tokens):
    return [t for t in tokens if len(t) > 1]


def remove_roman(tokens):
    regex = '^(?=[mdclxvi])m*(c[md]|d?c{0,3})(x[cl]|l?x{0,3})(i[xv]|v?i{0,3})$'
    return [t for t in tokens if not bool(re.search(re.compile(regex), t))]


# remove stopwords, símbolos, números e palavras com menos de duas letras
def filter_words(tokens):
    t1 = remove_stopwords(tokens)
    t2 = remove_pontuaction(t1)
    t3 = remove_one_letter(t2)

    return(remove_roman(t3))


# divide os tokens em listas de n palavras e salva em uma lista maior
def batch(tokens):
    if len(tokens) > 5000:
        n = 1000
    elif len(tokens) > 500:
        n = 100
    else:
        n = 10

    mod = len(tokens) % n
    out_range = math.ceil(len(tokens) / n)
    out_list = []
    start = 0
    stop = n

    for i in range(out_range):
        in_list = [tokens[j] for j in range(start, stop)]

        if i == (out_range - 2):
            stop += mod
        else:
            stop += n
        start += n
        out_list.append(in_list)
    return out_list


# usa o pacote TreeTagger para lematizar o texto
def tags(raw):
    tagger = TreeTagger(language='portuguese')
    return tagger.tag(raw.lower())


# salva os tokens lematizados
# busca por adjetivos (A), advérbios (R), substantivos (N) e verbos (V)
# e ignora as outras classes
def tags_to_token(raw):
    label = re.compile('^A|^R|^NC.P|^NCF|^V')
    tagged = tags(raw)
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


def convert_to_text(tokens):
    return nltk.Text(tokens)
