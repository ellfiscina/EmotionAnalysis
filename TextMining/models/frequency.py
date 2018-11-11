from nltk import FreqDist


class Frequency:
    def __init__(self, tokens):
        self.tokens = tokens
        self.dist = FreqDist(tokens)

    def lexical_diversity(self):
        tokens = self.tokens
        percentage = (len(set(tokens)) / len(tokens)) * 100
        return round(percentage, 2)

    def most_frequent(self, qtt):
        sortedToken = sorted(list(set(self.tokens)),
                             key=lambda token: self.dist[token],
                             reverse=True)
        frequent = [(token, self.dist[token]) for token in sortedToken[:qtt]]
        return frequent
