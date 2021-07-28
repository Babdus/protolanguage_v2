from typing import Set, Union, Iterable

from app.data.features import features_cache as fts
from app.data.pickles import feature_categories, ipa_rules, feature_subsets
from app.models.feature import Feature
from app.utils.colors import Colored


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
        return f"{Colored(self.__class__.__name__).yellow()}({args})"

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
