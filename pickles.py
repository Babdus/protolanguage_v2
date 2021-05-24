import pickle

def read_pickle(path):
    with open(path, 'rb') as f:
        obj = pickle.load(f)
    return obj

replace = read_pickle('data/pickles/ipa_char_replace_dict.pickle')
letters = read_pickle('data/pickles/ipa_letters_dicts.pickle')
modifiers = read_pickle('data/pickles/ipa_modifiers_dict.pickle')
ignore = read_pickle('data/pickles/ipa_ignore_symbols_set.pickle')
features_info = read_pickle('data/pickles/features_info.pickle')

ipa_rules = read_pickle('data/pickles/ipa_rules.pickle')
feature_subsets = read_pickle('data/pickles/feature_subsets.pickle')

feature_categories = ['place', 'secondary_place', 'manner', 'secondary_manner', 'airflow']
