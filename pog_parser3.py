from utils import Token
from parser_nodes import BinOpNode, StringNode, NumberNode, IdentNode

class Parser3:
    def __init__(self, tokens):
        self.tokens = tokens
        self.ast = {}
        self.idx = -1
        self.advance()

    def advance(self):
        self.idx+=1
        current = Token(self.tokens[self.idx])
        





def get_node(token):
    if token.type == 'OPERATOR':
        return BinOpNode(token)
    elif token.type == 'STRING':
        return StringNode(token)
    elif token.type in ('INTEGER', 'FLOAT'):
        return NumberNode(token)
    elif token.type == 'IDENT':
        return IdentNode(token)
