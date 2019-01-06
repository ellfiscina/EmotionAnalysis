from collections import Counter


def MostFrequent(emoList, qtt):
    labels = ['positivo', 'negativo', 'alegria', 'tristeza', 'nojo',
              'antecipação', 'medo', 'surpresa', 'confiança', 'raiva']
    emoCount = []

    for l in labels:
        # salva os 5 tokens mais comuns por emoção em uma lista
        emoCount.append(Counter(emoList[l]).most_common(qtt))

    # aplaina a lista
    flatList = [item for sublist in emoCount for item in sublist]

    # ordena a lista do maior para o menor
    sortedList = sorted(
        set(flatList), key=lambda tup: tup[1], reverse=True)

    # retorna os 5 tokens mais comuns
    return [i[0] for i in sortedList[:qtt]]
