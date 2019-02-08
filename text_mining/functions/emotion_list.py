from collections import defaultdict


def NewList(tokens, emotionList):
    emoList = defaultdict(list)

    # import code; code.interact(local=dict(globals(), **locals()))
    for t in tokens:
        for e in emotionList:
            x = False
            if('não ' in t):
                z = t[4:]
                x = True
            else:
                z = t
            if z in emotionList[e]:
                if(x):
                    emoList[revert_emotion(e)].append(t)
                else:
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
    elif emotion == 'repulsa':
        return 'confiança'
    elif emotion == 'confiança':
        return 'repulsa'
