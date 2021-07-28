from typing import Any

from app.data.pickles import asymmetric_feature_distance_map as afdm
from app.utils.colors import Colored


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
        return f"{Colored(self.__class__.__name__).cyan()}({args})"

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
