from app.models.language import Language


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
