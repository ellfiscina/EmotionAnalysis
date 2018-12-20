import csv
import copy
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
        self.emotionCounts = self.generate_emotion_count()
        self.wordCounts = self.generate_word_count()
        self.commonArray = self.most_common_array()

    def generate_word_count(self):
        labels = ['positivo', 'negativo', 'alegria', 'tristeza', 'nojo',
                  'antecipação', 'medo', 'surpresa', 'confiança', 'raiva']

        dataset = []
        temp_set = []
        emoCount = {}
        wordCount = {}

        for l in labels:
            temp = Counter(self.emoList[l])

            for key, val in temp.items():
                wordCount['name'] = key
                wordCount['value'] = val
                temp_set.append(copy.copy(wordCount))

            emoCount['name'] = l
            emoCount['children'] = temp_set
            dataset.append(copy.copy(emoCount))

        return '{ "name": "emotion", "children":' + str(dataset).replace('\'', '\"') + '}'

    def newList(self):
        emoList = defaultdict(list)
        for t in self.tokens:
            for e in self.emotionList:
                for w in self.emotionList[e]:
                    if w == t:
                        emoList[e].append(w)
        return emoList

    def generate_emotion_count(self):
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

    def most_common_array(self):
        labels = ['positivo', 'negativo', 'alegria', 'tristeza', 'nojo',
                  'antecipação', 'medo', 'surpresa', 'confiança', 'raiva']

        emoCount = []

        for l in labels:
            # salva os 5 tokens mais comuns por emoção em uma lista
            emoCount.append(Counter(self.emoList[l]).most_common(5))

        # aplaina a lista
        flatList = [item for sublist in emoCount for item in sublist]

        # ordena a lista do maior para o menor
        sortedList = sorted(set(flatList), key=lambda tup: tup[1], reverse=True)

        # retorna os 5 tokens mais comuns
        return [i[0] for i in sortedList[:5]]

    def to_dict(self):
        return {
            'emotionCount': self.emotionCounts,
            'wordCount': self.wordCounts
        }
