import copy
from collections import defaultdict, Counter
from django.core.exceptions import ObjectDoesNotExist
from text_mining.models import Word

labels = ['positivo', 'negativo', 'alegria', 'tristeza', 'nojo',
          'antecipação', 'medo', 'surpresa', 'confiança', 'raiva']


def generate_word_count(emoList):
    array_out = []

    for l in labels:
        array_in = []
        dict_out = {}

        temp = Counter(emoList[l])

        for key, val in temp.items():
            dict_in = {}
            dict_in['name'] = key
            dict_in['value'] = val
            array_in.append(copy.copy(dict_in))

        dict_out['name'] = l
        dict_out['children'] = array_in
        array_out.append(copy.copy(dict_out))

    dataset = '{ "name": "emotion", "children":' + \
        str(array_out).replace('\'', '\"') + '}'
    return dataset


def newList(tokens):
    emoList = defaultdict(list)

    for t in tokens:
        try:
            w = Word.objects.get(word=t)
        except ObjectDoesNotExist:
            continue

        for e in w.emotion_set.all():
            emoList[e.emotion].append(t)
    return emoList


def most_common_array(emoList):
    emoCount = []

    for l in labels:
        # salva os 5 tokens mais comuns por emoção em uma lista
        emoCount.append(Counter(emoList[l]).most_common(5))

    # aplaina a lista
    flatList = [item for sublist in emoCount for item in sublist]

    # ordena a lista do maior para o menor
    sortedList = sorted(
        set(flatList), key=lambda tup: tup[1], reverse=True)

    # retorna os 5 tokens mais comuns
    return [i[0] for i in sortedList[:5]]
