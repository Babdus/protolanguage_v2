from typing import Tuple

import numpy as np

from app.data.phonemes import empty_phoneme
from app.models.lexeme import Lexeme
from app.models.named_matrix import NamedMatrix


def calculate_lexeme_distance(
        source_lexeme: Lexeme,
        target_lexeme: Lexeme,
        phoneme_distance_matrix: NamedMatrix
) -> Tuple[float, Lexeme, Lexeme]:
    matrix = np.zeros((len(source_lexeme) + 1, len(target_lexeme) + 1))
    for i, source_phoneme in enumerate(source_lexeme):
        matrix[i + 1, 0] = matrix[i, 0] + phoneme_distance_matrix[source_phoneme, empty_phoneme]
    for j, target_phoneme in enumerate(target_lexeme):
        matrix[0, j + 1] = matrix[0, j] + phoneme_distance_matrix[empty_phoneme, target_phoneme]
    for j, target_phoneme in enumerate(target_lexeme):
        for i, source_phoneme in enumerate(source_lexeme):
            matrix[i + 1, j + 1] = min(
                matrix[i, j + 1] + phoneme_distance_matrix[source_phoneme, empty_phoneme],
                matrix[i + 1, j] + phoneme_distance_matrix[empty_phoneme, target_phoneme],
                matrix[i, j] + phoneme_distance_matrix[source_phoneme, target_phoneme]
            )
    return matrix[-1][-1] / (len(source_lexeme) + len(target_lexeme))
