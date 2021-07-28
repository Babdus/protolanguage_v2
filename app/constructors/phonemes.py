from typing import List

from munkres import Munkres

from app.data.phonemes import empty_phoneme
from app.models.language import Language
from app.models.named_matrix import NamedMatrix
from app.operations.phoneme import calculate_phoneme_distance
from app.utils.timing import timing


@timing
def construct_phoneme_distance_matrix(
        languages: List[Language],
        csv_path: str = None,
        vectorize: bool = False
) -> NamedMatrix:
    munkres = Munkres()
    all_phonemes = sorted(list({phone for lang in languages for lex in lang for phone in lex}))
    all_phonemes.append(empty_phoneme)
    matrix = NamedMatrix(
        column_names=all_phonemes,
        row_names=all_phonemes,
        function=calculate_phoneme_distance,
        args=[munkres],
        name='pdm',
        vectorize=vectorize
    )
    if csv_path:
        matrix.to_csv(csv_path)
    return matrix
