from typing import List

import pandas as pd

from app.models.lexeme import Synonyms, Lexeme
from app.models.language import Language
from app.models.tree import Tree
from app.models.named_matrix import NamedMatrix
from app.operations.language import calculate_language_distance
from app.operations.parser import ipa_string_to_lexeme
from app.utils.colors import Colored
from app.utils.timing import timing
from constructors.lexeme import reconstruct_lexeme
from operations.lexeme import calculate_lexeme_distance


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


def set_lexeme_to_descendants(meaning: str, lexeme: Lexeme, synonym: Lexeme, language: Language) -> None:
    if isinstance(language[meaning], Synonyms):
        if synonym in language[meaning]:
            language[meaning] = lexeme
            for child in language.get_child_languages():
                set_lexeme_to_descendants(meaning, lexeme, synonym, child)


def reconstruct_language(root: Language, pdm: NamedMatrix, threshold: float = 2.0) -> None:
    children = root.get_child_languages()

    # recursion
    for child in children:
        if len(child.lexemes) == 0:
            reconstruct_language(child, pdm, threshold=threshold)

    # calculate language distance
    language_distance = sum(edge.distance for edge in root.child_edges)

    # for each word pair:
    for key_word in (children[0] & children[1]):
        if (key_word in children[0]) and (key_word in children[1]):

            synonyms_1 = children[0][key_word]
            synonyms_2 = children[1][key_word]

            if not isinstance(synonyms_1, Synonyms):
                synonyms_1 = Synonyms([synonyms_1])
            if not isinstance(synonyms_2, Synonyms):
                synonyms_2 = Synonyms([synonyms_2])

            # calculate min word distance for each synonym pair
            min_word_distance = None
            min_word_pair = (Lexeme([]), Lexeme([]))
            for lexeme_1 in synonyms_1:
                for lexeme_2 in synonyms_2:
                    distance = calculate_lexeme_distance(lexeme_1, lexeme_2, pdm)
                    if min_word_distance is None or distance < min_word_distance:
                        min_word_distance = distance
                        min_word_pair = (lexeme_1, lexeme_2)

            if min_word_distance > language_distance * threshold:
                # set every synonym as the parent word
                root[key_word] = synonyms_1 + synonyms_2
            else:
                # reconstruct_lexeme
                proto_lexeme = reconstruct_lexeme(
                    min_word_pair[0],
                    min_word_pair[1],
                    children[0].parent_edge.distance,
                    children[1].parent_edge.distance,
                    pdm
                )
                root[key_word] = proto_lexeme

                # set this lexeme recursively to any child that had synonyms with this word
                for i, child in enumerate(children):
                    set_lexeme_to_descendants(key_word, proto_lexeme, min_word_pair[i], child)

        elif key_word in children[0]:
            root[key_word] = children[0][key_word]
        elif key_word in children[1]:
            root[key_word] = children[1][key_word]


@timing
def reconstruct_protolanguages(tree: Tree, pdm: NamedMatrix) -> Tree:
    reconstruct_language(tree.root, pdm)
    return tree
