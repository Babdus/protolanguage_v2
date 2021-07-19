from multiprocessing import Pool, cpu_count
from munkres import DISALLOWED
import numpy as np

from linguistics import Lexeme, empty_feature, empty_phoneme
from structures import NamedMatrix
from log_functions import colored

def calculate_phoneme_distance(ph1, ph2, munk):
    if ph1 == ph2:
        return 0
    set1 = ph1 - ph2
    set2 = ph2 - ph1
    list1 = list(set1) + [empty_feature] * len(set2)
    list2 = list(set2) + [empty_feature] * len(set1)
    matrix = [[f1.distance_to(f2, default=DISALLOWED) for f2 in list2] for f1 in list1]
    indexes = munk.compute(matrix)
    return sum(matrix[r][c] for r, c in indexes)


def calculate_lexeme_distance(
            source_lexeme: Lexeme,
            target_lexeme: Lexeme,
            phoneme_distance_matrix: NamedMatrix
    ) -> float:
    matrix = np.zeros((len(source_lexeme)+1, len(target_lexeme)+1))
    for i, source_phoneme in enumerate(source_lexeme):
        matrix[i+1, 0] = matrix[i, 0] + phoneme_distance_matrix[source_phoneme][empty_phoneme]
    for j, target_phoneme in enumerate(target_lexeme):
        matrix[0, j+1] = matrix[0, j] + phoneme_distance_matrix[empty_phoneme][target_phoneme]
    for j, target_phoneme in enumerate(target_lexeme):
        for i, source_phoneme in enumerate(source_lexeme):
            matrix[i+1, j+1] = min(
                matrix[i, j+1] + phoneme_distance_matrix[source_phoneme][empty_phoneme],
                matrix[i+1, j] + phoneme_distance_matrix[empty_phoneme][target_phoneme],
                matrix[i, j] + phoneme_distance_matrix[source_phoneme][target_phoneme]
            )
    return matrix[-1][-1], source_lexeme, target_lexeme


def calculate_language_distance(lang_1, lang_2, pdm):
    pool = Pool(cpu_count())
    args = [(lang_1[word], lang_2[word], pdm) for word in lang_1 & lang_2]
    dists = pool.starmap(calculate_lexeme_distance, args)
    pool.close()
    scaled_dists = [dist/(len(lex1)+len(lex2)) for dist, lex1, lex2 in dists]
    return sum(scaled_dists)/len(scaled_dists)
