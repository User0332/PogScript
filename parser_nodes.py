class AbstractNode:
    def __init__(self, tok, left = None, right = None):
        self.token = tok
        self.left = left
        self.right = right

class NumberNode(AbstractNode):
    pass

class BinOpNode(AbstractNode):
    pass

class StringNode(AbstractNode):
    pass

class IdentNode(AbstractNode):
    pass

