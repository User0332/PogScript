from utils import Token

class Tree:
	def __init__(self, root, parent=None):
		self.parent = parent
		self.root = Token(root)
		self.children = []

	def add_child(self, child):
		node = Tree(child, parent=self)
		self.children.append(node)
		return node

	def __repr__(self):
		_repr = "  "*(len(self.children))+str(self.root)
		if self.parent is None:
			_repr+="\n"
		for i, child in enumerate(self.children):
			_repr+=str(child)
			if _repr.endswith("\n") and i != len(self):
				_repr =_repr[:-1]
			if i == len(self):
				_repr+="\n"
			

		return _repr

	def __len__(self):
		return len(self.children)
			


tree = Tree([0, 0])

child  = tree.add_child([0, 1])

child2 = tree.add_child([1, 0])

grandchild = child.add_child([0, 2])

grandchild2 = child.add_child([1, 1])

print(tree)