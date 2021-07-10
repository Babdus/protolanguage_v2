from typing import Any, Callable, List, Dict
import pandas as pd
from linguistics import Language


class NamedRow(object):
    def __init__(
            self,
            column_names: List[Any],
            row_name: Any,
            function: Callable[..., Any],
            args: List[Any] = [],
            kwargs: Dict[str, Any] = {}
    ) -> None:
        self.column_names = column_names
        self.index_map = {column_name: i for i, column_name in enumerate(self.column_names)}
        self.row = []
        for column_name in self.column_names:
            value = function(row_name, column_name, *args, **kwargs)
            self.row.append(value)

    def __getitem__(self, index: Any) -> Any:
        return self.row.__getitem__(self.index_map[index])

    def __setitem__(self, index: Any, item: Any) -> None:
        self.row.__setitem__(self.index_map[index], item)

    def __delitem__(self, index: Any) -> None:
        self.row.__delitem__(self.index_map[index])

    def __len__(self) -> int:
        return self.row.__len__()


class NamedMatrix(object):
    def __init__(
            self,
            column_names: List[Any],
            row_names: List[Any],
            function: Callable[..., Any],
            args: List[Any] = [],
            kwargs: Dict[str, Any] = {}
    ) -> None:
        self.column_names = column_names
        self.row_names = row_names
        self.index_map = {row_name: i for i, row_name in enumerate(self.row_names)}
        self.matrix = []
        for row_name in self.row_names:
            row = NamedRow(self.column_names, row_name, function, args, kwargs)
            self.matrix.append(row)

    def __getitem__(self, index: Any) -> NamedRow:
        return self.matrix.__getitem__(self.index_map[index])

    def __setitem__(self, index: Any, item: Any) -> None:
        self.matrix.__setitem__(self.index_map[index], item)

    def __delitem__(self, index: Any) -> None:
        self.matrix.__delitem__(self.index_map[index])

    def __len__(self) -> int:
        return self.matrix.__len__()

    def get_inner_matrix(self) -> List[List]:
        inner_matrix = []
        for row in self.matrix:
            inner_matrix.append(row.row)
        return inner_matrix

    def to_csv(self, csv_path: str) -> None:
        string_column_names = [str(column_name) for column_name in self.column_names]
        string_row_names = [str(row_name) for row_name in self.row_names]
        df = pd.DataFrame(self.get_inner_matrix(), columns=string_column_names, index=string_row_names)
        df.to_csv(csv_path)


class Edge(object):
    def __init__(
            self,
            parent_language: Language,
            child_language: Language,
            distance: float = 0.0
        ) -> None:
        self.parent_language = parent_language
        self.child_language = child_language
        self.distance = distance


class Tree(object):
    def __init__(self, root_language: Language) -> None:
        self.root = root_language
        self.languages = set()
        self.leaves = set()
        self.edges = set()
        self._discover_descendants(self.root)

    def _discover_descendants(self, root: Language) -> None:
        for child_edge in root.child_edges:
            self.edges.add(child_edge)
            self.languages.add(child_edge.child_language)
            self._discover_descendants(child_edge.child_language)
            if child_edge.child_language.is_leaf():
                self.leaves.add(child_edge.child_language)
