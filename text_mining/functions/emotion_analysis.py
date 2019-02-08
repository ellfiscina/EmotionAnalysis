import copy
from collections import Counter


def generate_word_count(emoList):
    labels = ['positivo', 'negativo', 'alegria', 'tristeza', 'repulsa',
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

        dict_out['name'] = l.capitalize()
        dict_out['children'] = array_in
        array_out.append(copy.copy(dict_out))

    dataset = '{ "name": "Emoções", "children":' + \
        str(array_out).replace('\'', '\"') + '}'
    return dataset


def generate_emotion_distribution(emoList, tokens):
    # import code; code.interact(local=dict(globals(), **locals()))
    outter = {}

    for emo in emoList:
        inner = []
        for token in tokens:
            index = tokens.index(token)
            count = 0
            for t in token:
                if t in emoList[emo]:
                    count += 1
            inner.append([index, count])
        outter[emo] = inner
    return outter
