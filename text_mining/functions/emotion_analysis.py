import copy
from collections import defaultdict, Counter
from django.core.exceptions import ObjectDoesNotExist
from text_mining.models import Word


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


def generate_word_count(emoList):
    labels = ['positivo', 'negativo', 'alegria', 'tristeza', 'nojo',
              'antecipação', 'medo', 'surpresa', 'confiança', 'raiva']
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


def generate_emotion_distribution(emoList, sent_list):
    outter = {}
    for emo in emoList:
        inner = []

        for sent in sent_list:
            index = sent_list.index(sent)
            count = 0
            for t in sent:
                if t in emoList[emo]:
                    count += 1
            inner.append([index, count])
        outter[emo] = inner
    return outter
