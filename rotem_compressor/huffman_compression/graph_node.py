LEAF_SYMBOL = 1
NONLEAF_SYMBOL = 0

class Node:
    def __init__(self, left, right, data):
        self.left = left
        self.right = right
        self.data = data

    def __lt__(self, other):
        return self.data is not None and other.data is not None and self.data < other.data

    def print_tree(self, space, space_jump=10):
        space += space_jump
        if self.right:
            self.right.print_tree(space)
        print()
        for i in range(space_jump, space):
            print(end=" ")
        print(chr(self.data) if self.data else None)
        if self.left:
            self.left.print_tree(space)