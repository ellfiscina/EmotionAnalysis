from collections import defaultdict
import re


def NewList(tokens, emotionList):
    emoList = defaultdict(list)

    # import code; code.interact(local=dict(globals(), **locals()))
    for t in tokens:
        for e in emotionList:
            for w in emotionList[e]:
                if(bool(re.search(re.compile('não '), t))):
                    if w == re.sub(r'não ', '', t):
                        emoList[revert_emotion(e)].append(t)
                elif w == t:
                    emoList[e].append(t)
    return emoList


def revert_emotion(emotion):
    if emotion == 'positivo':
        return 'negativo'
    elif emotion == 'negativo':
        return 'positivo'
    elif emotion == 'alegria':
        return 'tristeza'
    elif emotion == 'tristeza':
        return 'alegria'
    elif emotion == 'antecipação':
        return 'surpresa'
    elif emotion == 'surpresa':
        return 'antecipação'
    elif emotion == 'medo':
        return 'raiva'
    elif emotion == 'raiva':
        return 'medo'
    elif emotion == 'nojo':
        return 'confiança'
    elif emotion == 'confiança':
        return 'nojo'
