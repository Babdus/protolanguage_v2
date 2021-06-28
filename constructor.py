import linguistics as ln
from pickles import asymmetric_feature_distance_map as afdm
import parser
import pandas as pd
import numpy as np
from munkres import Munkres, DISALLOWED
from log_functions import colored


def construct_languages(catalogue_path, min_words=40):
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
        languages.append(ln.Language(language_name, language_code, lexemes=lexemes))
    return languages

# languages = construct_languages('../Protolanguage/Data/words_and_languages/Catalogue.csv')
# for language in languages:
#     print(colored(language.code).yellow().bold())
#     print(colored(language.name).green())
#     print(colored(language[3].representation).blue().inverse())
#     print(colored(language[3].meaning).white().bold())
#     print(colored(language[3].name).red().bold().italic().dim())
# print(len(languages))

def phoneme_distance(ph1, ph2, munk):
    if ph1 == ph2:
        return 0
    set1 = ph1 - ph2
    set2 = ph2 - ph1
    list1 = list(set1) + [ln.features_cache['X']] * len(set2)
    list2 = list(set2) + [ln.features_cache['X']] * len(set1)
    matrix = [[afdm[(f1.code, f2.code)] if (f1.code, f2.code) in afdm else DISALLOWED for f2 in list2] for f1 in list1]
    indexes = munk.compute(matrix)
    return sum(matrix[r][c] for r, c in indexes)


def construct_phoneme_distance_matrix(languages, csv_path=None):
    munk = Munkres()
    all_phonemes = sorted(list({phoneme for language in languages for lexeme in language for phoneme in lexeme}))
    matrix = [[phoneme_distance(ph1, ph2, munk) for ph2 in all_phonemes] for ph1 in all_phonemes]
    all_symbols = list(map(lambda x: x.representation, all_phonemes))
    df = pd.DataFrame(matrix, columns=all_symbols, index=all_symbols)
    if csv_path:
        df.to_csv(csv_path)
    return df, matrix, all_phonemes
