import json

from constructors.languages import construct_languages, construct_language_distance_matrix, reconstruct_protolanguages
from constructors.phonemes import construct_phoneme_distance_matrix
from constructors.trees import construct_tree
from utils.io import tree_to_dict
from utils.timing import timing


@timing
def main():
    languages = construct_languages(catalogue_path='../data/catalogue.csv', min_words=205)
    phoneme_distance_matrix = construct_phoneme_distance_matrix(languages=languages)
    language_distance_matrix = construct_language_distance_matrix(languages=languages, pdm=phoneme_distance_matrix)
    tree = construct_tree(ldm=language_distance_matrix)
    tree_dict = tree_to_dict(tree.root)
    with open('../data/generated/tree2.json', 'w') as f:
        json.dump(tree_dict, f)
    tree = reconstruct_protolanguages(tree=tree, pdm=phoneme_distance_matrix)
    tree_dict = tree_to_dict(tree.root)
    with open('../data/generated/tree_with_languages2.json', 'w') as f:
        json.dump(tree_dict, f)


if __name__ == '__main__':
    main()
