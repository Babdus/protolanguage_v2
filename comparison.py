from multiprocessing import Pool, cpu_count

import linguistics as ln
from log_functions import colored


def calculate_lexeme_distance(word, lex_1, lex_2):
    return word, abs(len(lex_1) - len(lex_2))


def calculate_language_distance(lang_1, lang_2):
    pool = Pool(cpu_count)
    args = [(word, lang_1[word], lang_2[word]) for word in lang_1 & lang_2]
    return pool.starmap(calculate_lexeme_distance, args)