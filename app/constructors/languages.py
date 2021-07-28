from typing import List

import pandas as pd

from app.models.language import Language
from app.models.named_matrix import NamedMatrix
from app.operations.language import calculate_language_distance
from app.operations.parser import ipa_string_to_lexeme
from app.utils.colors import Colored
from app.utils.timing import timing


@timing
def construct_languages(catalogue_path: str, min_words: int = 40) -> List[Language]:
    df = pd.read_csv(catalogue_path, index_col='Code')
    df = df[df.index.notnull()]
    df.drop(['Family', 'Group', 'Code2'], axis=1, inplace=True)
    df = df[df['#'] > min_words]
    df.drop(['#'], axis=1, inplace=True)
    df = df.fillna('')

    languages = []
    for language_code, row in df.iterrows():
        language_name = row['Language']
        row.drop(['Language'], inplace=True)
        lexemes = []
        for meaning in row.index:
            word = row[meaning]
            if len(word) == 0:
                continue
            try:
                lexeme = ipa_string_to_lexeme(word, meaning, language_code)
            except ValueError as e:
                print(Colored(str(e)).red().bold(), word, meaning, language_name)
            else:
                lexemes.append(lexeme)
        languages.append(Language(language_name, language_code, lexemes=lexemes))
    return languages


@timing
def construct_language_distance_matrix(
        languages: List[Language],
        pdm: NamedMatrix,
        csv_path: str = None,
        vectorize: bool = False
) -> NamedMatrix:
    language_codes = list(map(lambda l: l.code, languages))
    matrix = NamedMatrix(
        column_names=language_codes,
        row_names=language_codes,
        function=calculate_language_distance,
        args=[pdm],
        column_items=languages,
        row_items=languages,
        name='ldm',
        vectorize=vectorize
    )
    if csv_path:
        matrix.to_csv(csv_path)
    return matrix
