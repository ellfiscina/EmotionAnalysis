from collections import defaultdict


def NewList(tokens, emotionList):
    emoList = defaultdict(list)

    for t in tokens:
        for e in emotionList:
            for w in emotionList[e]:
                if w == t:
                    emoList[e].append(t)
    return emoList
