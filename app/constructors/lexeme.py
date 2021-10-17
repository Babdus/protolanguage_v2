from models.lexeme import Lexeme
from models.named_matrix import NamedMatrix


def reconstruct_lexeme(
        lexeme_1: Lexeme,
        lexeme_2: Lexeme,
        distance_1: float,
        distance_2: float,
        phoneme_distance_matrix: NamedMatrix
) -> Lexeme:
    return Lexeme(
        phonemes=lexeme_1.phonemes+lexeme_2.phonemes,
        meaning=lexeme_1.meaning,
        language_code=lexeme_1.language_code
    )
