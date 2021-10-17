from typing import List, Union, Set, Dict

from .feature import Feature
from .lexeme import Lexeme, Synonyms
from .phoneme import Phoneme
from app.utils.colors import Colored


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

    def __init__(self, name: str, code: str, lexemes: List[Union[Lexeme, Synonyms]] = None) -> None:
        if lexemes is None:
            lexemes = []
        self.name = name
        self.code = code
        self.lexemes = lexemes
        for lexeme in self.lexemes:
            lexeme.set_language_code(code)
        self._redefine_lexemes_dict()
        self.parent_edge = None
        self.child_edges = []

    def _redefine_lexemes_dict(self) -> None:
        self.lexemes_dict = {lexeme.meaning: lexeme for lexeme in self.lexemes}
        self.lexeme_index_dict = {lexeme.meaning: i for i, lexeme in enumerate(self.lexemes)}

    def __repr__(self) -> str:
        args = f"'{self.name}', '{self.code}', {self.lexemes}"
        return f"{Colored(self.__class__.__name__).blue()}({args})"

    def __str__(self) -> str:
        """Return name, code and the vocabulary of this language"""
        return f"name: {self.name}, code: {self.code}, vocabulary: {self.get_vocabulary()}"

    def __getitem__(self, index: Union[int, str]) -> Union[Lexeme, Synonyms]:
        """Return self.lexemes[index]"""
        if isinstance(index, int):
            return self.lexemes.__getitem__(index)
        else:
            return self.lexemes_dict.__getitem__(index)

    def __setitem__(self, index: Union[int, str], item: Union[Lexeme, Synonyms]) -> None:
        """self.lexemes[index] = item"""
        if isinstance(index, int):
            meaning = self.lexemes.__getitem__(index).meaning
        else:
            meaning = index
            if meaning in self.lexeme_index_dict:
                index = self.lexeme_index_dict[meaning]
            else:
                index = len(self.lexemes)
        if meaning in self.lexemes_dict:
            self.lexemes_dict.__delitem__(meaning)
        if index == len(self.lexemes):
            self.lexemes.append(item)
        else:
            self.lexemes.__setitem__(index, item)
        self.lexemes_dict[item.meaning] = item
        self.lexeme_index_dict[item.meaning] = index

    def __delitem__(self, index: int) -> None:
        """del self.lexemes[index]"""
        meaning = self.lexemes.__getitem__(index).meaning
        self.lexemes_dict.__delitem__(meaning)
        self.lexemes.__delitem__(index)
        self.lexeme_index_dict = {lexeme.meaning: i for i, lexeme in enumerate(self.lexemes)}

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

    def insert(self, index: int, item: Union[Lexeme, Synonyms]) -> None:
        """self.lexemes.insert(index, item)"""
        self.lexemes.insert(index, item)
        self._redefine_lexemes_dict()

    def append(self, item: Union[Lexeme, Synonyms]) -> None:
        """self.lexemes.append(item)"""
        self.lexemes.append(item)
        self._redefine_lexemes_dict()

    def get_vocabulary(self) -> List[str]:
        """Return a list of words this language contains in the IPA transcription."""
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
