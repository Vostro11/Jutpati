
class Tree:
    def __init__(self, cargo, left=None,middle=None, right=None):
        self.cargo = cargo
        self.left = left
        self.middle = middle
        self.right = right

    def __str__(self):
        return str(self.cargo)


def make_tree(n=1):
    if n <= 5:
        return Tree(n, make_tree(n + 1), make_tree(n + 2), make_tree(n + 3))


def print_tree(tree):
    if tree is None:
        return
    print(tree.cargo)
    print('l', tree.left)
    print('m', tree.middle)
    print('r', tree.right)
    print_tree(tree.left)


print_tree(make_tree())
