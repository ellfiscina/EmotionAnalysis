from nltk import ngrams, FreqDist


def max_dist(emoList):
    x = {}
    for e in emoList:
        fd = FreqDist(emoList[e])
        m = fd.max()
        x[m] = fd.freq(m)
    return max(x, key=lambda k: x[k])


def n_grams(text, emoList):
    target_word = max_dist(emoList)
    fd = FreqDist(ng for ng in ngrams(text, 5) if target_word in ng)
    x = [' '.join(hit) for hit in fd]
    return x[:10]


def concordance(text, dist):
    target_word = dist.max()
    return text.concordance(target_word)


def similar(text, emoList):
    return text.similar(max_dist(emoList))
