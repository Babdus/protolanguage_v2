from app.operations.lexeme import calculate_lexeme_distance


def calculate_language_distance(lang_1, lang_2, pdm):
    dists = [calculate_lexeme_distance(lang_1[word], lang_2[word], pdm) for word in lang_1 & lang_2]
    # pool = Pool(1)
    # args = [(lang_1[word], lang_2[word], pdm) for word in lang_1 & lang_2]
    # dists = pool.starmap(calculate_lexeme_distance, args)
    # pool.close()
    return sum(dists) / len(dists)
