from linguistics import Language, Phoneme, empty_phoneme
from structures import NamedMatrix
from comparison import calculate_phoneme_distance, calculate_language_distance
from pickles import asymmetric_feature_distance_map as afdm
import parser
import pandas as pd
import numpy as np
from munkres import Munkres
from log_functions import colored
from typing import List


def construct_languages(catalogue_path, min_words=200):
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
                lexeme = parser.ipa_string_to_lexeme(word, meaning, language_code)
            except ValueError as e:
                print(colored(str(e)).red().bold(), word, meaning, language_name)
            lexemes.append(lexeme)
        languages.append(Language(language_name, language_code, lexemes=lexemes))
    return languages


def construct_phoneme_distance_matrix(
            languages: List[Language],
            csv_path: str = None
    ) -> NamedMatrix:
    munk = Munkres()
    all_phonemes = sorted(list({phon for lang in languages for lex in lang for phon in lex}))
    all_phonemes.append(empty_phoneme)
    matrix = NamedMatrix(
        column_names=all_phonemes,
        row_names=all_phonemes,
        function=calculate_phoneme_distance,
        args=[munk]
    )
    if csv_path:
        matrix.to_csv(csv_path)
    return matrix


def construct_language_distance_matrix(
            languages: List[Language],
            pdm: NamedMatrix,
            csv_path: str = None
    ) -> NamedMatrix:
    language_codes = list(map(lambda l: l.code, languages))
    matrix = NamedMatrix(
        column_names=language_codes,
        row_names=language_codes,
        function=calculate_language_distance,
        args=[pdm],
        column_items=languages,
        row_items=languages
    )
    if csv_path:
        matrix.to_csv(csv_path)
    return matrix
