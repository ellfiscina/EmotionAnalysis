import nltk
from treetagger import TreeTagger


class PreProcess:
    stopwords = nltk.corpus.stopwords.words('portuguese')

    def __init__(self, raw):
        self.raw = raw.lower()
        self.tokens = self.tokenize()
        self.filtered = self.filter()
        self.text = self.convert_to_text()

    def tokenize(self):
        return nltk.word_tokenize(self.raw)

    def filter(self):
        return [t for t in self.tokens
                if t not in self.stopwords and t.isalpha()]

    def convert_to_text(self):
        return nltk.Text(self.tokens)


class POSTag(PreProcess):
    tagger = TreeTagger(language='portuguese')

    def __init__(self, raw):
        super().__init__(raw)

    def negations(tokens):
        words = []
        for i in range(0, len(tokens)):
            if tokens[i] == 'não' and tokens[i + 1].isalpha():
                words.append(' '.join(tokens[i:i + 2]))
            elif tokens[i - 1] == 'não':
                pass
            else:
                words.append(tokens[i])
        return words

    def tags(self, raw):
        return self.tagger.tag(raw)
