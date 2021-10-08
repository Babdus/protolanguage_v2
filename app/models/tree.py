from .language import Language


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
