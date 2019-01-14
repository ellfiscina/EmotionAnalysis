def LexicalDiversity(tokens):
    # qtd de tokens únicos / qtd total de tokens
    percentage = (len(set(tokens)) / len(tokens)) * 100
    return round(percentage, 2)
