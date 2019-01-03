import nltk
import re
from treetagger import TreeTagger


class PreProcess:

    def __init__(self, raw):
        self.stopwords = self.extend_stopwords()
        self.raw = raw.lower()
        self.tokens = self.tokenize()
        self.filtered = self.filter(self.tokens)
        self.text = self.convert_to_text()

    def extend_stopwords(self):
        stopwords = nltk.corpus.stopwords.words('portuguese')
        words = ['é', 'quê', 'aí', 'lá', 'ia', 'aqui', 'ah', 'oh', 'ali']
        stopwords.extend(words)
        return stopwords

    def tokenize(self):
        return nltk.word_tokenize(self.raw)

    def filter(self, tokens):
        return [t for t in tokens
                if t not in self.stopwords and t.isalpha()]

    def convert_to_text(self):
        return nltk.Text(self.tokens)

    def to_dict(self):
        return {
            'tokens': self.tokens,
            'filtered': self.filtered,
            'uniq_tokens': set(self.tokens),
            'uniq_filtered': set(self.filtered)
        }


class POSTag(PreProcess):
    tagger = TreeTagger(language='portuguese')
    label = re.compile('^A|^R|^NC.P|^NCF|^V')

    def __init__(self, raw):
        super().__init__(raw)
        self.tagged = self.tags(raw)
        self.tokens = self.tags_to_token()
        self.filtered = self.filter(self.negations(self.tokens))

    def tags(self, raw):
        return self.tagger.tag(raw)

    def tags_to_token(self):
        tokens = []
        for tag in self.tagged:
            if(bool(re.search(self.label, tag[1])) is False or
               tag[2] == '<unknown>'):
                tokens.append(tag[0].lower())
            else:
                tokens.append(tag[2])
        return tokens

    def negations(self, tokens):
        words = []
        for i in range(0, len(tokens)):
            if tokens[i] == 'não' and tokens[i + 1].isalpha():
                words.append(' '.join(tokens[i:i + 2]))
            elif tokens[i - 1] == 'não':
                pass
            else:
                words.append(tokens[i])
        return words

    def to_dict(self):
        return {
            'tokens': self.tokens,
            'filtered': self.filtered,
        }
