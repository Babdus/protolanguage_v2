from typing import List

from .feature import Feature
from .phoneme import Phoneme
from app.utils.colors import Colored


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
        return f"{Colored(self.__class__.__name__).green()}({args})"

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

    def set_language_code(self, code: str) -> None:
        self.language_code = code

    def _redefine_name(self) -> None:
        self.name = ", ".join([phoneme.name for phoneme in self.phonemes])

    def _redefine_representation(self) -> None:
        self.representation = ''.join([phoneme.representation for phoneme in self.phonemes])


class Synonyms(object):
    def __init__(self, lexemes: List[Lexeme]) -> None:
        self.meaning = lexemes[0].meaning
        self.lexemes = lexemes
        self._redefine_representation()

    def __repr__(self) -> str:
        args = f"{self.lexemes}"
        return f"{Colored(self.__class__.__name__).magenta()}({args})"

    def __str__(self) -> str:
        """Return self.representation"""
        return self.representation

    def __getitem__(self, index: int) -> Lexeme:
        """Return self.lexemes[index]"""
        return self.lexemes.__getitem__(index)

    def __setitem__(self, index: int, item: Lexeme) -> None:
        """self.lexemes[index] = item"""
        self.lexemes.__setitem__(index, item)
        self._redefine_representation()

    def __delitem__(self, index: int) -> None:
        """del self.lexemes[index]"""
        self.lexemes.__delitem__(index)
        self._redefine_representation()

    def __len__(self) -> int:
        """Return len(self.lexemes)"""
        return self.lexemes.__len__()

    def __contains__(self, item: Lexeme) -> bool:
        """Return item in self.lexemes"""
        return item in self.lexemes

    def __add__(self, other: 'Synonyms') -> 'Synonyms':
        """Return new Synonyms with lexemes from both self and other"""
        return Synonyms(self.lexemes + other.lexemes)

    def insert(self, index: int, item: Lexeme) -> None:
        """self.lexemes.insert(index, item)"""
        self.lexemes.insert(index, item)
        self._redefine_representation()

    def append(self, item: Lexeme) -> None:
        """self.lexemes.append(item)"""
        self.lexemes.append(item)
        self._redefine_representation()

    def set_language_code(self, code: str) -> None:
        for lexeme in self.lexemes:
            lexeme.set_language_code(code)

    def _redefine_representation(self) -> None:
        self.representation = '|'.join([lexeme.representation for lexeme in self.lexemes])
