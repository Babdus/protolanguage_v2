from __future__ import annotations

import pickle
from collections import Iterable
from typing import Any, Set, Union, List, Dict

from log_functions import colored
from pickles import asymmetric_feature_distance_map as afdm
from pickles import feature_categories, features_info, ipa_rules, feature_subsets


def save(obj: Any, path: str):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)


def load(path: str):
    with open(path, 'wb') as f:
        obj = pickle.load('path')
    return obj


class Feature(object):
    """Feature(name, code, category, index)

    A Feature object represents a single phonetic feature, a characteristic of
    any speech sound (phone). Sounds may have (and in reality allways have) more
    than one phonetic feature.

    Parameters
    ----------
    name : str
        Linguistic name of the phonetic feature. Should have capitalized first
        letter and be unique.
    code : str
        A two capital letter identifier of this feature. Should be unique.
    category : str
        One of these five: place, secondary_place, manner, secondary_manner,
        airflow. Should be lowercase.
    index : int
        A number reference to the index of thies feature in the matrix of the
        feature distances. Should be unique.

    Attributes
    ----------
    name : str
        Human-readable identifier of this feature.
    code : str
        two-letter identifier of this feature.
    category : str
        One of these five: place, secondary_place, manner, secondary_manner,
        airflow.
        * place : An articulation place of a sound in with toung, lips, pharinx,
                 other place or combination of places in the vocal tract.
        * secondary_place : A place in a vocal tract which is involved alongside
                           the primary place but with less intensity.
        * manner : A method with which the sound is produced in the vocal tract.
        * secondary_manner : A secondary, helping method in the producing the
                             sound.
        * airflow : A type of action for providing needed air to the vocal tract
                    for producing the sound.
    index : int
        A number identifier of this feature, referencing to the matrix of the
        feature distances.

    See Also
    --------
    Phoneme : A representation of the speech sound.
    Lexeme : A representation of the word with its linguistic features.
    Language : A representation of the language as a set of words and node in
               the evolutionary tree of languages.

    Notes
    -----
    If you are using ipa_string_to_lexeme function of the parser module, it is
    recommended not to create Feature objct if not absolutely necessary. Most
    probably there is already created exactly the same Feature object and stored
    in the features_cache variable of the parser module.

    Examples
    --------
    >>> alveolar = Feature('Alveolar', 'AL', 'place', 1)

    >>> alveolar
    Feature('Alveolar', 'AL', 'place', 1)

    >>> plosive = Feature('Plosive', 'PL', 'manner', 30)

    >>> plosive
    Feature('Plosive', 'PL', 'manner', 30)

    >>> alveolar == plosive
    False

    >>> alveolar_2 = Feature('Alveolar', 'AL', 'place', 1)

    >>> alveolar == alveolar_2
    True
    """

    def __init__(self, name: str, code: str, category: str, index: int) -> None:
        self.name = name.capitalize()
        self.code = code.upper()
        self.category = category.lower()
        self.index = index

    def __repr__(self) -> str:
        args = f"'{self.name}', '{self.code}', '{self.category}', {self.index}"
        return f"{colored(self.__class__.__name__).cyan()}({args})"

    def __eq__(self, other: 'Feature') -> bool:
        return isinstance(other, self.__class__) and self.code == other.code

    def __ne__(self, other: 'Feature') -> bool:
        return not (isinstance(other, self.__class__) and self.code == other.code)

    def __lt__(self, other: 'Feature') -> bool:
        return self.index < other.index

    def __le__(self, other: 'Feature') -> bool:
        return self.index <= other.index

    def __gt__(self, other: 'Feature') -> bool:
        return self.index > other.index

    def __ge__(self, other: 'Feature') -> bool:
        return self.index >= other.index

    def __hash__(self) -> int:
        return hash(self.code)

    def distance_to(self, other: 'Feature', default: Any = None) -> Any:
        if (self.code, other.code) in afdm:
            return afdm[(self.code, other.code)]
        return default


features_cache = {k: Feature(v[1], k, v[2], v[0]) for k, v in features_info.items()}
fts = features_cache
empty_feature = features_cache['X']


class Phoneme(object):
    """Phoneme(features, representation='')

    A Phoneme object represents a single speech sound, a building block for any
    word in any language.

    Parameters
    ----------
    features : set of Feature objects
        Set of features that defines this sound.
    representation : str, optional
        IPA (International Phonetic Alphabet) trancription of this sound.

    Attributes
    ----------
    features : set of Feature objects
        Set of features that defines this sound.
    representation : str
        IPA transcription of this phoneme.
    categories : list of strings
        List of all phonetic feature categories in which the features of this
        sound are.
    name : str
        A human-readable linguistic name of this sound that is comprised of
        the comma-separated names of features of this sound.
    places : list of Feature objects
        List of all features of this phoneme (are in the attribute `features`)
        with the category 'place'. May be empty.
    place : Feature object
        A first (sorted by `index` attribute of the Feature) feature of this
        phoneme that is of category 'place'. Is the equvalent of `places[0]`.
        If there is no feature with the category 'place' than an empty Feature
        object is returned: Feature('', 'X', '', 0).
    secondary_places : list of Feature objects
        List of all features of this phoneme (are in the attribute `features`)
        with the category 'secondary_place'. May be empty.
    secondary_place : Feature object
        A first (sorted by `index` attribute of the Feature) feature of this
        phoneme that is of category 'secondary_place'. Is the equvalent of
        `secondary_places[0]`. If there is no feature with the category
        'secondary_place' than an empty Feature object is returned:
        Feature('', 'X', '', 0).
    manners : list of Feature objects
        List of all features of this phoneme (are in the attribute `features`)
        with the category 'manner'. May be empty.
    manner : Feature object
        A first (sorted by `index` attribute of the Feature) feature of this
        phoneme that is of category 'manner'. Is the equvalent of `manners[0]`.
        If there is no feature with the category 'manner' than an empty Feature
        object is returned: Feature('', 'X', '', 0).
    secondary_manners : list of Feature objects
        List of all features of this phoneme (are in the attribute `features`)
        with the category 'secondary_manner'. May be empty.
    secondary_manner : Feature object
        A first (sorted by `index` attribute of the Feature) feature of this
        phoneme that is of category 'secondary_manner'. Is the equvalent of
        `secondary_manners[0]`. If there is no feature with the category
        'secondary_manner' than an empty Feature object is returned:
        Feature('', 'X', '', 0).
    airflows : list of Feature objects
        List of all features of this phoneme (are in the attribute `features`)
        with the category 'airflow'. May be empty.
    airflow : Feature object
        A first (sorted by `index` attribute of the Feature) feature of this
        phoneme that is of category 'airflow'. Is the equvalent of `airflows[0]`.
        If there is no feature with the category 'airflow' than an empty Feature
        object is returned: Feature('', 'X', '', 0).

    See Also
    --------
    Feature : A representation of the distinct characteristics of the sound.
    Lexeme : A representation of the word with its linguistic features.
    Language : A representation of the language as a set of words and node in
               the evolutionary tree of languages.

    Examples
    --------
    >>> alveolar = Feature('Alveolar', 'AL', 'place', 1)

    >>> plosive = Feature('Plosive', 'PL', 'manner', 30)

    >>> t = Phoneme({alveolar, plosive}, representation='t')

    >>> t
    Phoneme({Feature('Plosive', 'PL', 'manner', 30), Feature('Alveolar', 'AL',
    'place', 1)}, representation='t')

    >>> t_2 = Phoneme({plosive, alveolar})

    >>> t_2
    Phoneme({Feature('Plosive', 'PL', 'manner', 30), Feature('Alveolar', 'AL',
    'place', 1)}, representation='')

    >>> t == t_2
    True

    >>> t.name
    'Alveolar Plosive'

    >>> t.categories
    ['manner', 'place']

    >>> t.places
    [Feature('Alveolar', 'AL', 'place', 1)]

    >>> t.place
    Feature('Alveolar', 'AL', 'place', 1)

    >>> t.airflow
    Feature('', 'X', '', 0)
    """

    def __init__(self, features: Set[Feature], representation: str = '') -> None:
        self.features = features
        self.representation = representation
        self.categories = sorted(feature.category for feature in self.features)
        self._redefine_name_and_category_attributes()

    def _redefine_name_and_category_attributes(self) -> None:
        for category in feature_categories:
            similar_features = [ft for ft in self.features if ft.category == category]
            setattr(self, f'{category}s', similar_features)
            feature = similar_features[0] if len(similar_features) > 0 else Feature('', 'X', '', 0)
            setattr(self, category, feature)
        feature_names = []
        for cat in feature_categories:
            f_name = ' '.join([f.name for f in eval(f'self.{cat}s', {'self': self})])
            feature_names.append(f_name)
        self.name = " ".join([name for name in feature_names if name != ''])

    def __repr__(self) -> str:
        args = f"{self.features}, representation='{self.representation}'"
        return f"{colored(self.__class__.__name__).yellow()}({args})"

    def __str__(self) -> str:
        """Return self.representation"""
        return self.representation

    def __eq__(self, other: 'Phoneme') -> bool:
        return isinstance(other, self.__class__) and self.features == other.features

    def __ne__(self, other: 'Phoneme') -> bool:
        return not isinstance(other, self.__class__) or self.features != other.features

    def __lt__(self, other: 'Phoneme') -> bool:
        return hash(self.name) < hash(other.name)

    def __le__(self, other: 'Phoneme') -> bool:
        return hash(self.name) <= hash(other.name)

    def __gt__(self, other: 'Phoneme') -> bool:
        return hash(self.name) > hash(other.name)

    def __ge__(self, other: 'Phoneme') -> bool:
        return hash(self.name) >= hash(other.name)

    def __hash__(self) -> int:
        return hash(self.name)

    def __getitem__(self, index: int) -> Feature:
        """Return self.features[index]"""
        return sorted(self.features)[index]

    def __contains__(self, item: Union[Feature, Iterable[Feature]]) -> bool:
        if isinstance(item, Feature):
            return item in self.features
        elif isinstance(item, Iterable):
            return all(f in self.features for f in item)
        return False

    def __sub__(self, other: 'Phoneme') -> Set[Feature]:
        """Return set of features that are in this phoneme and not in other"""
        return self.features - other.features

    def __and__(self, other: 'Phoneme') -> Set[Feature]:
        """Return a union of features set from this and other phoneme"""
        return self.features & other.features

    def __or__(self, other: 'Phoneme') -> Set[Feature]:
        """Return an intersection of features set from this and other phoneme"""
        return self.features | other.features

    def __xor__(self, other: 'Phoneme') -> Set[Feature]:
        """Return set of features that are in this or the other phoneme but not in both"""
        return self.features ^ other.features

    def add(self, feature: Feature, redefine: bool = True) -> None:
        """Add a feature to the features of this phoneme."""
        self.features.add(feature)
        if redefine:
            self._redefine_name_and_category_attributes()

    def remove(self, feature: Feature, redefine: bool = True) -> None:
        """Remove a feature from the features of this phoneme."""
        if feature in self.features:
            self.features.remove(feature)
        if redefine:
            self._redefine_name_and_category_attributes()

    def replace(self, feature1: Feature, feature2: Feature, redefine: bool = True) -> None:
        if feature1 in self:
            self.remove(feature1, redefine=False)
            self.add(feature2, redefine=False)
        if redefine:
            self._redefine_name_and_category_attributes()

    def set_place(self, feature: Feature, redefine: bool = True) -> None:
        """Set an articulation place of this phoneme to given feature."""
        for place_feature in self.places:
            self.remove(place_feature)
        self.add(feature)
        if redefine:
            self._redefine_name_and_category_attributes()

    def advance(self, redefine: bool = True) -> None:
        for place_feature in self.places:
            if place_feature == fts['PA']:
                self.add(fts['AL'], redefine=False)
            elif place_feature == fts['NE'] and self.is_vowel():
                self.add(fts['PZ'], redefine=False)
            elif place_feature == fts['VE'] and self.is_vowel():
                self.add(fts['VZ'], redefine=False)
                self.replace(place_feature, fts['NE'], redefine=False)
            else:
                replace_with = fts[ipa_rules['advance'][place_feature.code]]
                self.replace(place_feature, replace_with, redefine=False)
        if redefine:
            self._redefine_name_and_category_attributes()

    def lower(self, redefine: bool = True) -> None:
        for manner_feature in self.manners:
            replace_with = fts[ipa_rules['lower'][manner_feature.code]]
            self.replace(manner_feature, replace_with, redefine=False)
        if redefine:
            self._redefine_name_and_category_attributes()

    def upper(self, redefine: bool = True) -> None:
        for manner_feature in self.manners:
            replace_with = fts[ipa_rules['upper'][manner_feature.code]]
            self.replace(manner_feature, replace_with, redefine=False)
        if redefine:
            self._redefine_name_and_category_attributes()

    def dentalize(self, redefine: bool = True) -> None:
        for manner_feature in self.places:
            replace_with = fts[ipa_rules['dentalize'][manner_feature.code]]
            self.replace(manner_feature, replace_with, redefine=False)
        if redefine:
            self._redefine_name_and_category_attributes()

    def is_vowel(self) -> bool:
        return len({fts[f_code] for f_code in feature_subsets['vowel_manners']} & self.features) > 0

    def __len__(self) -> int:
        """Return a number of features that this phoneme has."""
        return len(self.features)


empty_phoneme = Phoneme(set())


class Lexeme(object):
    """Lexeme(phonemes, meaning='', language_code='')

    A Lexeme object represents a single word, but not only as a plain string,
    but with a phonetic representation, with meaning, and with indication of the
    language it belongs to. The building blocks of lexeme are phonemes, as are
    characters for strings.

    Parameters
    ----------
    phonemes : list of Phoneme objects
        An ordered list of phonemes that makes this word as whole.
    meaning : str, optional
        The meaning of this word in English. Lowercase.
    language_code : str, optional
        The code of the language that has this word in it's vocabulary. Codes
        are generaly of two letter format of ISO 639-1, three letter formats of
        ISO 639-3 or ISO 639-2, or of compound xxx-yyy or xxx-yyy-zzz formats.
        The langauge codes are in one-to-one correspondence with the Wiktionary
        lanuage codes. For detailed information visit:
        https://en.wiktionary.org/wiki/Wiktionary:Languages#Language_codes.
        And for the complete list of language codes and corresponding languages
        visit https://en.wiktionary.org/wiki/Wiktionary:List_of_languages.
        Lowercase.

    Attributes
    ---------
    phonemes : list of Phoneme objects
        A list of phonemes (sounds that makes this word up).
    meaning : str
        An english lowercase word denoting the meaning of this lexeme. If not
        provided in the constructor, it will be an empty string.
    language_code : str
        The identificator of the language to which this lexeme belongs. See
        above `language_code` in parameters section for more information.
    name : str
        A phonetic description of this lexeme. It consists of comma-separated
        names of individual phonemes, which in turn consist of space-separated
        phonetic feature names.
    representation : str
        An IPA (International Phonetic Alphabet) transcription of this word. It
        may be inclomplete - lacking some characters if any of the Phonemes lack
        `representation` attribute themselves.

    See Also
    --------
    Feature : A representation of the distinct characteristics of the sound.
    Phoneme : A representation of the speech sound.
    Language : A representation of the language as a set of words and node in
               the evolutionary tree of languages.

    Examples
    --------
    >>> al = Feature('Alveolar', 'AL', 'place', 1)

    >>> pl = Feature('Plosive', 'PL', 'manner', 30)

    >>> op = Feature('open', 'OP', 'manner', 27)

    >>> vo = Feature('voiced', 'VO', 'airflow', 42)

    >>> pa = Feature('palatal', 'PA', 'place', 28)

    >>> d = Phoneme({al, pl, vo}, representation='d')

    >>> a = Phoneme({pa, op, vo}, representation='a')

    >>> da = Lexeme([d, a], meaning='and', language_code='ka')

    >>> da
    Lexeme([Phoneme({Feature('Plosive', 'PL', 'manner', 30), Feature('Alveolar',
    'AL', 'place', 1), Feature('Voiced', 'VO', 'airflow', 42)}, representation='
    d'), Phoneme({Feature('Open', 'OP', 'manner', 27), Feature('Voiced', 'VO', '
    airflow', 42), Feature('Palatal', 'PA', 'place', 28)}, representation='a')],
    meaning='and', language_code='ka')

    >>> da.name
    'Alveolar Plosive Voiced,Palatal Open Voiced'

    >>> da.representation
    'da'
    """

    def __init__(self, phonemes: List[Phoneme], meaning: str = '', language_code: str = '') -> None:
        self.phonemes = phonemes
        self.meaning = meaning
        self.language_code = language_code
        self._redefine_name()
        self._redefine_representation()

    def __repr__(self) -> str:
        args = f"{self.phonemes}, meaning='{self.meaning}', language_code='{self.language_code}'"
        return f"{colored(self.__class__.__name__).green()}({args})"

    def __str__(self) -> str:
        """Return self.representation"""
        return self.representation

    def __eq__(self, other: 'Lexeme') -> bool:
        return isinstance(other, self.__class__) and self.phonemes == other.phonemes

    def __ne__(self, other: 'Lexeme') -> bool:
        return not isinstance(other, self.__class__) or self.phonemes != other.phonemes

    def __lt__(self, other: 'Lexeme') -> bool:
        return hash(self.name) < hash(other.name)

    def __le__(self, other: 'Lexeme') -> bool:
        return hash(self.name) <= hash(other.name)

    def __gt__(self, other: 'Lexeme') -> bool:
        return hash(self.name) > hash(other.name)

    def __ge__(self, other: 'Lexeme') -> bool:
        return hash(self.name) >= hash(other.name)

    def __hash__(self) -> int:
        return hash(self.name)

    def __getitem__(self, index: int) -> Phoneme:
        """Return self.phonemes[index]"""
        return self.phonemes.__getitem__(index)

    def __setitem__(self, index: int, item: Phoneme) -> None:
        """self.phonemes[index] = item"""
        self.phonemes.__setitem__(index, item)
        self._redefine_name()
        self._redefine_representation()

    def __delitem__(self, index: int) -> None:
        """del self.phonemes[index]"""
        self.phonemes.__delitem__(index)
        self._redefine_name()
        self._redefine_representation()

    def __len__(self) -> int:
        """Return len(self.phonemes)"""
        return self.phonemes.__len__()

    def __contains__(self, item: Phoneme) -> bool:
        """Return item in self.phonemes"""
        return item in self.phonemes

    def insert(self, index: int, item: Phoneme) -> None:
        """self.phonemes.insert(index, item)"""
        self.phonemes.insert(index, item)
        self._redefine_name()
        self._redefine_representation()

    def append(self, item: 'Phoneme') -> None:
        """self.phonemes.append(item)"""
        self.phonemes.append(item)
        self._redefine_name()
        self._redefine_representation()

    def _redefine_name(self) -> None:
        self.name = ", ".join([phoneme.name for phoneme in self.phonemes])

    def _redefine_representation(self) -> None:
        self.representation = ''.join([phoneme.representation for phoneme in self.phonemes])


class Language(object):
    """Language(name, code, lexemes=[])

    The Language object represents an instance of one natural human language
    with its basic vocabulary (for example Swadesh list) and with a possibility
    to take place in an evolutionary tree of languages.

    Parameters
    ----------
    name : str
        A human name of this language. Fisrt letter capitalized.
    code : str
        The standardized code of this language. Codes are generaly of two letter
        format of ISO 639-1, three letter formats of ISO 639-3 or ISO 639-2, or
        of compound xxx-yyy or xxx-yyy-zzz formats. The langauge codes are in
        one-to-one correspondence with the Wiktionary lanuage codes. For
        detailed information visit:
        https://en.wiktionary.org/wiki/Wiktionary:Languages#Language_codes.
        And for the complete list of language codes and corresponding languages
        visit https://en.wiktionary.org/wiki/Wiktionary:List_of_languages.
        Lowercase. Should be unique.
    lexemes : list of Lexeme objects, optional
        A list of words that this language has. The words themselves should be
        an instances of Lexeme classes. default: empty list.

    Attributes
    ----------
    name : str
        A human name of this language.
    code : str
        A unique identifier of this language. See above `code` in parameters
        section for more information.
    lexemes : list of Lexeme objects
        A list of lexemes (words) that belong to this language.
    parent_edge : Edge object
        An edge that represents a relationship between two languages. In this
        case, on the other end of this edge is a proposed parent language of
        this language.
    child_edges : list of Edge objects
        The list of edges that connect thsi language to its child languages.

    See Also
    --------
    Feature : A representation of the distinct characteristics of the sound.
    Phoneme : A representation of the speech sound.
    Lexeme : A representation of the word with its linguistic features.
    Edge : A representation of the connection between two languages.
    Tree : A representation of the evolutionary language tree.

    Examples
    --------
    >>> al = Feature('Alveolar', 'AL', 'place', 1)

    >>> pl = Feature('Plosive', 'PL', 'manner', 30)

    >>> op = Feature('open', 'OP', 'manner', 27)

    >>> vo = Feature('voiced', 'VO', 'airflow', 42)

    >>> pa = Feature('palatal', 'PA', 'place', 28)

    >>> d = Phoneme({al, pl, vo}, representation='d')

    >>> a = Phoneme({pa, op, vo}, representation='a')

    >>> t = Phoneme({al, pl}, representation='t')

    >>> da = Lexeme([d, a], meaning='and', language_code='ka')

    >>> data = Lexeme([d, a, t, a], meaning='dave', language_code='ka')

    >>> georgian = Language('Georgian', 'ka', lexemes=[da, data])
    Language('Georgian', 'ka', [Lexeme([Phoneme({Feature('Alveolar', 'AL', 'plac
    e', 1), Feature('Voiced', 'VO', 'airflow', 42), Feature('Plosive', 'PL', 'ma
    nner', 30)}, representation='d'), Phoneme({Feature('Open', 'OP', 'manner', 2
    7), Feature('Voiced', 'VO', 'airflow', 42), Feature('Palatal', 'PA', 'place'
    , 28)}, representation='a')], meaning='and', language_code='ka'), Lexeme([Ph
    oneme({Feature('Alveolar', 'AL', 'place', 1), Feature('Voiced', 'VO', 'airfl
    ow', 42), Feature('Plosive', 'PL', 'manner', 30)}, representation='d'), Phon
    eme({Feature('Open', 'OP', 'manner', 27), Feature('Voiced', 'VO', 'airflow',
    42), Feature('Palatal', 'PA', 'place', 28)}, representation='a'), Phoneme({F
    eature('Alveolar', 'AL', 'place', 1), Feature('Plosive', 'PL', 'manner', 30)
    }, representation='t'), Phoneme({Feature('Open', 'OP', 'manner', 27), Featur
    e('Voiced', 'VO', 'airflow', 42), Feature('Palatal', 'PA', 'place', 28)}, re
    presentation='a')], meaning='dave', language_code='ka')])

    >>> georgian[0]
    Lexeme([Phoneme({Feature('Alveolar', 'AL', 'place', 1), Feature('Voiced', 'V
    O', 'airflow', 42), Feature('Plosive', 'PL', 'manner', 30)}, representation=
    'd'), Phoneme({Feature('Open', 'OP', 'manner', 27), Feature('Voiced', 'VO',
    'airflow', 42), Feature('Palatal', 'PA', 'place', 28)}, representation='a')]
    , meaning='and', language_code='ka')
    """

    def __init__(self, name: str, code: str, lexemes: List[Lexeme] = None) -> None:
        if lexemes is None:
            lexemes = []
        self.name = name
        self.code = code
        self.lexemes = lexemes
        for lexeme in self.lexemes:
            lexeme.language_code = code
        self._redefine_lexemes_dict()
        self.parent_edge = None
        self.child_edges = []

    def _redefine_lexemes_dict(self) -> None:
        self.lexemes_dict = {lexeme.meaning: lexeme for lexeme in self.lexemes}

    def __repr__(self) -> str:
        args = f"'{self.name}', '{self.code}', {self.lexemes}"
        return f"{colored(self.__class__.__name__).blue()}({args})"

    def __str__(self) -> str:
        """Return name, code and the vocabulary of this language"""
        return f"name: {self.name}, code: {self.code}, vocabulary: {self.get_vocabulary()}"

    def __getitem__(self, index: Union[int, str]) -> Lexeme:
        """Return self.lexemes[index]"""
        if isinstance(index, int):
            return self.lexemes.__getitem__(index)
        else:
            return self.lexemes_dict.__getitem__(index)

    def __setitem__(self, index: int, item: Lexeme) -> None:
        """self.lexemes[index] = item"""
        meaning = self.lexemes.__getitem__(index).meaning
        self.lexemes_dict.__delitem__(meaning)
        self.lexemes.__setitem__(index, item)
        self.lexemes_dict[item.meaning] = item

    def __delitem__(self, index: int) -> None:
        """del self.lexemes[index]"""
        meaning = self.lexemes.__getitem__(index).meaning
        self.lexemes_dict.__delitem__(meaning)
        self.lexemes.__delitem__(index)

    def __len__(self) -> int:
        """Return len(self.lexemes)"""
        return self.lexemes.__len__()

    def __contains__(self, item: Union[Lexeme, str]) -> bool:
        """Return item in self.lexemes"""
        if isinstance(item, Lexeme):
            return item in self.lexemes
        elif isinstance(item, str):
            return item in self.lexemes_dict
        return False

    def __and__(self, other: 'Language') -> Set[str]:
        """Return a set of word meanings that are in both languages"""
        return set(self.lexemes_dict) & set(other.lexemes_dict)

    def __or__(self, other: 'Language') -> Set[str]:
        """Return a set of word meanings that are in any of these languages"""
        return set(self.lexemes_dict) | set(other.lexemes_dict)

    def insert(self, index: int, item: Lexeme) -> None:
        """self.lexemes.insert(index, item)"""
        self.lexemes.insert(index, item)

    def append(self, item: Lexeme) -> None:
        """self.lexemes.append(item)"""
        self.lexemes.append(item)

    def get_vocabulary(self) -> List[str]:
        """Return a list of words this language contains in the IPA trancription."""
        return [str(lexeme) for lexeme in self.lexemes]

    def get_dictionary(self) -> Dict[str, str]:
        """Return a dictionary of the words this language contains with keys in
        English and values with IPA transcriptions of these words."""
        return self.lexemes_dict

    def get_parent_language(self) -> 'Language':
        """Return a parent language of this language if set, otherwise return None."""
        return self.parent_edge.parent_language if self.parent_edge else None

    def get_child_languages(self) -> List['Language']:
        """Return a list of child languages that this language has"""
        return [edge.child_language for edge in self.child_edges]

    def is_leaf(self) -> bool:
        """Check if this language is a leaf node in the tree (has no child
        languages)"""
        return len(self.child_edges) == 0

    def is_root(self) -> bool:
        """Check if this language is a root node in the tree (has no parent
        language)"""
        return self.parent_edge is None
