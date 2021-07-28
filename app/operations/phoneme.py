from munkres import DISALLOWED

from app.data.features import empty_feature


def calculate_phoneme_distance(ph1, ph2, munkres):
    if ph1 == ph2:
        return 0
    set1 = ph1 - ph2
    set2 = ph2 - ph1
    list1 = list(set1) + [empty_feature] * len(set2)
    list2 = list(set2) + [empty_feature] * len(set1)
    matrix = [[f1.distance_to(f2, default=DISALLOWED) for f2 in list2] for f1 in list1]
    indexes = munkres.compute(matrix)
    return sum(matrix[r][c] for r, c in indexes)
