from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist
from text_mining.models import Word


def NewList(tokens):
    emoList = defaultdict(list)

    for t in tokens:
        try:
            w = Word.objects.get(word=t)
        except ObjectDoesNotExist:
            continue

        for e in w.emotion_set.all():
            emoList[e.emotion].append(t)
    return emoList
