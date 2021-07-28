from typing import Any, Callable, List, Dict, Tuple

import numpy as np
import pandas as pd


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
            vectorize: bool = False
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

        if vectorize:
            self.broadcast_function = np.frompyfunc(function, 2 + len(args) + len(kwargs), 1)
            self.matrix = self.broadcast_function(self.np_row_items, self.np_column_items[:, None], *args, **kwargs)
        else:
            self.matrix = np.array(
                [
                    [function(row_item, column_item, *args, **kwargs) for row_item in self.row_items]
                    for column_item in self.column_items
                ]
            )

    def __getitem__(self, index: Tuple[Any, Any]) -> Any:
        return self.matrix[self.row_index_map[index[0]], self.column_index_map[index[1]]]

    def __setitem__(self, index: Tuple[Any, Any], item: Any) -> None:
        self.matrix[self.row_index_map[index[0]], self.column_index_map[index[1]]] = item

    def __delitem__(self, index: Tuple[Any, Any]) -> None:
        del self.matrix[self.row_index_map[index[0]], self.column_index_map[index[1]]]

    def __len__(self) -> int:
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
