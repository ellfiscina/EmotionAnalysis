import csv
from collections import defaultdict, Counter


class Analysis():
    wordList = defaultdict(list)
    emotionList = defaultdict(list)

    with open('media/TextMining/emolex_pt.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['present']) == 1:
                wordList[row['word']].append(row['emotion'])
                emotionList[row['emotion']].append(row['word'])

    def __init__(self, tokens):
        self.tokens = tokens
        self.emoList = self.newList()
        self.emotionCounts = self.generate_count_with_negation()
        self.wordCounts = self.generate_count()

    def generate_count(self):
        labels = ['positivo', 'negativo', 'alegria', 'tristeza', 'nojo',
                  'antecipação', 'medo', 'surpresa', 'confiança', 'raiva']

        emoCount = {}

        for l in labels:
            emoCount[l] = Counter(self.emoList[l])

        count = [{'name': key, 'value': val} for key, val in emoCount.items()]
        return count

    def newList(self):
        emoList = defaultdict(list)
        for t in self.tokens:
            for e in self.emotionList:
                for w in self.emotionList[e]:
                    if w == t:
                        emoList[e].append(w)
        return emoList

    def generate_count_with_negation(self):
        t = self.tokens
        wordList = self.wordList
        emoCount = Counter()
        for i in range(len(t) - 1):
            if len(wordList[t[i]]) > 0:
                if t[i - 1] == 'não':
                    emoCount += Counter(self.revert_emotion(wordList[t[i]]))
                else:
                    emoCount += Counter(wordList[t[i]])
        return emoCount

    def revert_emotion(wordList):
        newList = []
        for w in wordList:
            if w == 'positivo':
                newList.append('negativo')
            elif w == 'negativo':
                newList.append('positivo')
            elif w == 'alegria':
                newList.append('tristeza')
            elif w == 'tristeza':
                newList.append('alegria')
            elif w == 'antecipação':
                newList.append('surpresa')
            elif w == 'surpresa':
                newList.append('antecipação')
            elif w == 'medo':
                newList.append('raiva')
            elif w == 'raiva':
                newList.append('medo')
            elif w == 'nojo':
                newList.append('confiança')
            elif w == 'confiança':
                newList.append('nojo')
        return newList

    def to_dict(self):
        return {
            'emotionCount': self.emotionCounts,
            'wordCount': self.wordCounts
        }
