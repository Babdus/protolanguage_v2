from typing import Any, Callable, List, Dict, Tuple

import numpy as np
import pandas as pd

from linguistics import Language


class NamedRow(object):
    def __init__(
            self,
            column_names: List[Any],
            row_name: Any,
            function: Callable[..., Any],
            args: List[Any] = None,
            kwargs: Dict[str, Any] = None,
            column_items: List[Any] = None,
            row_item: Any = None,
            printing: bool = False
    ) -> None:
        if kwargs is None:
            kwargs = {}
        if args is None:
            args = []
        self.column_names = column_names
        self.row_name = row_name
        self.index_map = {column_name: i for i, column_name in enumerate(self.column_names)}

        self.column_items = self.column_names if not column_items else column_items
        self.row_item = self.row_name if not row_item else row_item

        self.row = []
        for i, column_item in enumerate(self.column_items):
            print(self.row_name, '\t', self.column_names[i], end='\r') if printing else None
            value = function(self.row_item, column_item, *args, **kwargs)
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
            args: List[Any] = None,
            kwargs: Dict[str, Any] = None,
            column_items: List[Any] = None,
            row_items: List[Any] = None,
            name: str = None,
            printing: bool = False
    ) -> None:
        self.name = self.__name__ if name is None else name
        if kwargs is None:
            kwargs = {}
        if args is None:
            args = []
        self.column_names = column_names
        self.row_names = row_names
        self.row_index_map = {row_name: i for i, row_name in enumerate(self.row_names)}
        self.column_index_map = {column_name: i for i, column_name in enumerate(self.column_names)}

        self.row_items = self.row_names if not row_items else row_items
        self.column_items = self.column_names if not column_items else column_items
        self.np_row_items = np.array(self.row_items, dtype=object)
        self.np_column_items = np.array(self.column_items, dtype=object)

        self.broadcast_function = np.frompyfunc(function, 2 + len(args) + len(kwargs), 1)
        self.matrix = self.broadcast_function(self.np_row_items, self.np_column_items[:, None], *args, **kwargs)

    def getitem(self, row_index: Any, column_index: Any) -> Any:
        return self.matrix[self.row_index_map[row_index], self.column_index_map[column_index]]

    def setitem(self, row_index: Any, column_index: Any, item: Any) -> None:
        self.matrix[self.row_index_map[row_index], self.column_index_map[column_index]] = item

    def delitem(self, row_index: Any, column_index: Any,) -> None:
        del self.matrix[self.row_index_map[row_index], self.column_index_map[column_index]]

    def len(self) -> int:
        return len(self.matrix)

    def shape(self) -> Tuple[int, int]:
        return self.matrix.shape

    def get_inner_matrix(self) -> np.ndarray:
        return self.matrix

    def to_csv(self, csv_path: str) -> None:
        string_column_names = [str(column_name) for column_name in self.column_names]
        string_row_names = [str(row_name) for row_name in self.row_names]
        df = pd.DataFrame(self.matrix, columns=string_column_names, index=string_row_names)
        df.to_csv(csv_path)


class NamedMatrix2(object):
    def __init__(
            self,
            column_names: List[Any],
            row_names: List[Any],
            function: Callable[..., Any],
            args: List[Any] = None,
            kwargs: Dict[str, Any] = None,
            column_items: List[Any] = None,
            row_items: List[Any] = None,
            printing: bool = False
    ) -> None:
        if kwargs is None:
            kwargs = {}
        if args is None:
            args = []
        self.column_names = column_names
        self.row_names = row_names
        self.index_map = {row_name: i for i, row_name in enumerate(self.row_names)}

        self.row_items = self.row_names if not row_items else row_items
        self.column_items = self.column_names if not column_items else column_items

        self.matrix = []
        for i, row_item in enumerate(self.row_items):
            row = NamedRow(column_names=self.column_names,
                           row_name=self.row_names[i],
                           function=function,
                           args=args,
                           kwargs=kwargs,
                           column_items=self.column_items,
                           row_item=row_item,
                           printing=printing)
            self.matrix.append(row)

    def __getitem__(self, index: Any) -> NamedRow:
        return self.matrix.__getitem__(self.index_map[index])

    def __setitem__(self, index: Any, item: Any) -> None:
        self.matrix.__setitem__(self.index_map[index], item)

    def __delitem__(self, index: Any) -> None:
        self.matrix.__delitem__(self.index_map[index])

    def __len__(self) -> int:
        return self.matrix.__len__()

    def get_inner_matrix(self) -> List[List[Any]]:
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
