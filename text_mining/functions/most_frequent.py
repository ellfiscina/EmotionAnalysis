from collections import Counter


def MostFrequent(tokens, qtt):
    emoCount = []
    # salva os 5 tokens mais comuns por emoção em uma lista
    emoCount.append(Counter(tokens).most_common(qtt))

    # aplaina a lista
    flatList = [item for sublist in emoCount for item in sublist]

    # retorna os 5 tokens mais comuns
    return [i[0] for i in flatList]
