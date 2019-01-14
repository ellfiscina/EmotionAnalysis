import nltk
import math
# from treetagger import TreeTagger


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


def batch(tokens):
    mod = len(tokens) % 1000
    out_range = math.ceil(len(tokens) / 1000)
    out_list = []
    start = 0
    stop = 1000
    for i in range(out_range):
        in_list = []

        for j in range(start, stop):
            in_list.append(tokens[j])

        if i == (out_range - 2):
            stop += mod
        else:
            stop += 1000
        start += 1000
        out_list.append(in_list)
    return out_list


# def tags(raw):
#     tagger = TreeTagger(language='portuguese')
#     return tagger.tag(raw.lower())


# def tags_to_token(raw):
#     tagged = tags(raw)
#     label = re.compile('^A|^R|^NC.P|^NCF|^V')
#     tokens = []
#     for tag in tagged:
#         if(bool(re.search(label, tag[1])) is False or
#            tag[2] == '<unknown>'):
#             tokens.append(tag[0].lower())
#         else:
#             tokens.append(tag[2])
#     return tokens


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
