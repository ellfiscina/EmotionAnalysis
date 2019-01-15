from collections import defaultdict
import csv


# gera um dicionário com listas contendo as palavras que denotam cada emoção
def Emolex():
    emotionList = defaultdict(list)

    with open('text_mining/static/emolex_pt.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['present']) == 1:
                emotionList[row['emotion']].append(row['word'])

    return emotionList
