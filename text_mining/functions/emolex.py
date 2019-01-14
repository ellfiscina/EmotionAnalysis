from collections import defaultdict
import csv


def Emolex():
    emotionList = defaultdict(list)

    with open('text_mining/static/emolex_pt.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['present']) == 1:
                emotionList[row['emotion']].append(row['word'])

    return emotionList
