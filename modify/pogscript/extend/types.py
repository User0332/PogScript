class NewType:
    def __init__(self, keyword, token_name, derived_class):
        self.keyword = keyword
        self.name = token_name
        self._class = derived_class