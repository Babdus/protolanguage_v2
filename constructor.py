import linguistics as ln
import parser
import pandas as pd
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
