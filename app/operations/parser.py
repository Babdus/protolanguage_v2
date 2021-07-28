from app.data.features import features_cache
from app.data.pickles import replace, letters, modifiers, ignore
from app.models.lexeme import Lexeme
from app.models.phoneme import Phoneme
from app.utils.colors import Colored


def replace_non_ipa(string):
    return [replace[ch] if ch in replace else ch for ch in string]


def group_with_modifiers(chars):
    symbols = []
    for char in chars:
        if len(symbols) > 0 and char in modifiers:
            symbols[-1]['modifiers'].add(char)
        elif char in letters:
            symbols.append({'letter': char, 'modifiers': set()})
        elif char in ignore:
            continue
        else:
            print(Colored(str(hex(ord(char)))).green().bold())
            raise ValueError(f"{Colored(char).red()}, context: {chars}")
    return symbols


def group_single_phoneme_symbols(symbols):
    gathered_symbols = []
    i = 0
    while i < len(symbols):
        if i < len(symbols) - 1:
            double_letter = symbols[i]['letter'] + symbols[i + 1]['letter']
            if double_letter in letters and i < len(symbols) - 1:
                double_modifiers = symbols[i]['modifiers'] | symbols[i + 1]['modifiers']
                symbol = {'letter': double_letter, 'modifiers': double_modifiers}
                gathered_symbols.append(symbol)
                i += 2
                continue
        gathered_symbols.append(symbols[i])
        i += 1
    return gathered_symbols


def symbol_to_phoneme(symbol):
    feature_codes = letters[symbol['letter']]
    representation = f"{symbol['letter']}{''.join(symbol['modifiers'])}"
    features = {features_cache[code] for code in feature_codes}
    phoneme = Phoneme(features, representation=representation)
    for modifier in symbol['modifiers']:
        modifier_info = modifiers[modifier]
        actions = modifier_info['actions']
        for action, arg_feature_code in actions:
            if len(arg_feature_code) > 0:
                arg_feature = features_cache[arg_feature_code]
                getattr(phoneme, action)(arg_feature)
            else:
                getattr(phoneme, action)()
    return phoneme


def ipa_string_to_lexeme(ipa_string, meaning, language_code):
    ipa_chars = replace_non_ipa(ipa_string)
    ipa_symbols = group_with_modifiers(ipa_chars)
    ipa_gathered_symbols = group_single_phoneme_symbols(ipa_symbols)
    try:
        phonemes = [symbol_to_phoneme(symbol) for symbol in ipa_gathered_symbols]
    except KeyError as e:
        print(Colored(str(e)).red(), Colored(ipa_string).green(), Colored(str(ipa_gathered_symbols)).magenta())
    else:
        lexeme = Lexeme(phonemes, meaning=meaning, language_code=language_code)
        return lexeme


def phoneme_to_ipa_symbol(phoneme):
    if phoneme.representation != '':
        return phoneme.representation
    pass
