import nltk
from nltk import ngrams, FreqDist
from nltk.collocations import *


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


def concordance(ci, word, width=75, lines=25):
    """
    Rewrite of nltk.text.ConcordanceIndex.print_concordance that returns results
    instead of printing them.

    See:
    http://www.nltk.org/api/nltk.html#nltk.text.ConcordanceIndex.print_concordance
    """
    half_width = (width - len(word) - 2) // 2
    context = width // 4  # approx number of words of context

    results = []
    offsets = ci.offsets(word)
    if offsets:
        lines = min(lines, len(offsets))
        for i in offsets:
            if lines <= 0:
                break
            left = (' ' * half_width +
                    ' '.join(ci._tokens[i - context:i]))
            right = ' '.join(ci._tokens[i + 1:i + context])
            left = left[-half_width:]
            right = right[:half_width]
            results.append('%s %s %s' % (left, ci._tokens[i], right))
            lines -= 1

    return results[:10]


def collocations(tokens):
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(tokens)
    colls = finder.nbest(bigram_measures.likelihood_ratio, 10)

    return [' '.join(c) for c in colls]
