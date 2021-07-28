import numpy as np

from app.models.edge import Edge
from app.models.language import Language
from app.models.named_matrix import NamedMatrix
from app.models.tree import Tree
from app.utils.timing import timing


@timing
def construct_tree(
        ldm: NamedMatrix
) -> Tree:
    language_codes = ldm.column_names.copy()
    languages = ldm.column_items.copy()
    n = len(language_codes)
    delta = {}
    d = np.array(ldm.get_inner_matrix())
    ij_language = None

    while n > 1:
        # 1 Compute Q matrix
        Q = (d * (n - 2)) - np.sum(d, axis=0).reshape(1, n) - np.sum(d, axis=1).reshape(n, 1)
        np.fill_diagonal(Q, 0)

        # 2 Find pair with minimal value in Q
        i, j = np.unravel_index(Q.argmin(), Q.shape)

        # 3 Create parent node for minimal found pair and assign edge lengths
        ij_name = str(language_codes[i]) + '.' + str(language_codes[j])
        dist_i_ij = d[i, j] / 2 + ((np.sum(d[i]) - np.sum(d[j])) / (2 * (n - 2)) if n != 2 else 0)
        dist_j_ij = d[i, j] - dist_i_ij

        delta[(language_codes[i], ij_name)] = dist_i_ij
        delta[(language_codes[j], ij_name)] = dist_j_ij

        # 3.1 Create parent language object and connect it with its children languages
        ij_language = Language(ij_name, ij_name)

        language_codes.append(ij_name)
        languages.append(ij_language)

        edge_ij_i = Edge(
            parent_language=ij_language,
            child_language=languages[i],
            distance=dist_i_ij
        )
        languages[i].parent_edge = edge_ij_i
        edge_ij_j = Edge(
            parent_language=ij_language,
            child_language=languages[j],
            distance=dist_j_ij
        )
        languages[j].parent_edge = edge_ij_j
        ij_language.child_edges = [edge_ij_i, edge_ij_j]

        # 4 Calculate distances to other nodes from new one
        dists_to_ij = (d[i] + d[j] - d[i, j]) / 2

        # 5 Add row and column to d for new node
        d_new = np.zeros((n + 1, n + 1))
        d_new[:-1, :-1] = d
        d = d_new

        # 6 Set new distances to the new node in d
        d[:-1, -1] = dists_to_ij
        d[-1, :-1] = dists_to_ij

        # 6 Remove columns and rows for already parented nodes
        d = np.delete(d, (i, j), axis=0)
        d = np.delete(d, (i, j), axis=1)

        if i > j:
            del language_codes[i]
            del language_codes[j]
            del languages[i]
            del languages[j]
        else:
            del language_codes[j]
            del language_codes[i]
            del languages[j]
            del languages[i]

        n = len(language_codes)

    return Tree(root_language=ij_language) if ij_language is not None else None
