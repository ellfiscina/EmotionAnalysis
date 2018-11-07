from nltk import FreqDist


class Frequency:
    def __init__(self):
        self.dist = []

    def tokens_frequency(self, tokens):
        self.dist = FreqDist(tokens)

    def lexical_diversity(tokens):
        uniq = len(set(tokens))
        total = len(tokens)
        return (uniq / total) * 100

    def most_frequent(self, tokens, qtt):
        sortedToken = sorted(list(set(tokens)),
                             key=lambda token: self.dist[token],
                             reverse=True)
        frequent = [(token, self.dist[token]) for token in sortedToken[:qtt]]
        return frequent
