from multiprocessing import Pool, cpu_count
from munkres import DISALLOWED

import linguistics as ln
from log_functions import colored

def calculate_phoneme_distance(ph1, ph2, munk):
    if ph1 == ph2:
        return 0
    set1 = ph1 - ph2
    set2 = ph2 - ph1
    list1 = list(set1) + [ln.empty_feature] * len(set2)
    list2 = list(set2) + [ln.empty_feature] * len(set1)
    matrix = [[f1.distance_to(f2, default=DISALLOWED) for f2 in list2] for f1 in list1]
    indexes = munk.compute(matrix)
    return sum(matrix[r][c] for r, c in indexes)


def calculate_lexeme_distance(word, lex_1, lex_2):





    return word, abs(len(lex_1) - len(lex_2))


def calculate_language_distance(lang_1, lang_2):
    pool = Pool(cpu_count)
    args = [(word, lang_1[word], lang_2[word]) for word in lang_1 & lang_2]
    return pool.starmap(calculate_lexeme_distance, args)
