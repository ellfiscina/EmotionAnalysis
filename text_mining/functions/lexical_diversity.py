def LexicalDiversity(tokens):
    percentage = (len(set(tokens)) / len(tokens)) * 100
    return round(percentage, 2)
