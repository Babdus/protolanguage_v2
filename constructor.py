from linguistics import Language, Phoneme, empty_phoneme
from structures import NamedMatrix, Tree, Edge
from comparison import calculate_phoneme_distance, calculate_language_distance
from pickles import asymmetric_feature_distance_map as afdm
import parser
import pandas as pd
import numpy as np
from munkres import Munkres
from log_functions import colored
from typing import List


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


def construct_tree(
        ldm: NamedMatrix
    ) -> Tree:
    language_codes = ldm.column_names.copy()
    languages = ldm.column_items.copy()
    n = len(language_codes)
    delta = {}
    d = np.array(ldm.get_inner_matrix())

    while n > 1:
        #1 Compute Q matrix
        Q = (d * (n-2)) - np.sum(d, axis=0).reshape(1, n) - np.sum(d, axis=1).reshape(n, 1)
        np.fill_diagonal(Q, 0)

        #2 Find pair with minimal value in Q
        i, j = np.unravel_index(Q.argmin(), Q.shape)

        #3 Create parent node for minimal found pair and assign edge lengths
        ij_name = language_codes[i]+'.'+language_codes[j]
        dist_i_ij = d[i, j]/2 + ( ( np.sum(d[i]) - np.sum(d[j]) )/(2*(n-2)) if n != 2 else 0 )
        dist_j_ij = d[i, j] - dist_i_ij

        delta[(language_codes[i], ij_name)] = dist_i_ij
        delta[(language_codes[j], ij_name)] = dist_j_ij

        ij_language = Language(ij_name, ij_name)

        language_codes.append(ij_name)
        languages.append(ij_language)

        edge_ij_i = Edge(
            parent_language=ij_language,
            child_language=languages[i],
            distance=dist_i_ij
        )
        languages[i].parent_edge = edge_ij_i
        edge_ij_j = Edge(
            parent_language=ij_language,
            child_language=languages[j],
            distance=dist_j_ij
        )
        languages[j].parent_edge = edge_ij_j
        ij_language.child_edges = [edge_ij_i, edge_ij_j]

        #4 Calculate distances to other nodes from new one
        dists_to_ij = (d[i] + d[j] - d[i, j])/2

        #5 Add row and column to d for new node
        d_new = np.zeros((n+1, n+1))
        d_new[:-1, :-1] = d
        d = d_new

        #6 Set new distances to the new node in d
        d[:-1, -1] = dists_to_ij
        d[-1, :-1] = dists_to_ij

        #6 Remove columns and rows for already parented nodes
        d = np.delete(d, (i, j), axis=0)
        d = np.delete(d, (i, j), axis=1)

        if i > j:
            del language_codes[i]
            del language_codes[j]
            del languages[i]
            del languages[j]
        else:
            del language_codes[j]
            del language_codes[i]
            del languages[j]
            del languages[i]

        n = len(language_codes)

    return Tree(root_language=ij_language)
