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


def n_grams(text, target_word, n):
    fd = FreqDist(ng for ng in ngrams(text, n) if target_word in ng)
    x = [' '.join(hit) for hit in fd]
    return x


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


def treeword(text, word):
    ngrams = n_grams(text, word, 10)
    grams = [gram for gram in ngrams if word in gram[0:len(word)]]

    array_in = []
    dict_out = {}

    for g in grams[:10]:
        dict_in = {}

        dict_in['name'] = g.replace(word + ' ', '')
        dict_in['value'] = 1

        array_in.append(dict_in)

    dict_out['name'] = word
    dict_out['children'] = array_in

    return dict_out
