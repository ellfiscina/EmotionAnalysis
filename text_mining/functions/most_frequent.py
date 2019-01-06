from nltk import FreqDist


def MostFrequent(tokens, qtt):
    dist = FreqDist(tokens)
    sortedToken = sorted(list(set(tokens)),
                         key=lambda token: dist[token],
                         reverse=True)
    frequent = [{"text": token, "value": dist[token]}
                for token in sortedToken[:qtt]]
    return frequent
