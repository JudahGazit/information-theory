import queue

from rotem_compressor.data_models.tree_node import Node


class Dictionary:
    def __init__(self, dictionary_size, tree):
        self.dictionary_size = dictionary_size
        self.data = [None] * self.dictionary_size
        self.construct_dictionary(tree)

    def construct_dictionary(self, tree, prefix=''):
        if tree:
            if tree.left is None and tree.right is None:
                self.data[tree.data] = prefix
            self.construct_dictionary(tree.left, prefix + '0')
            self.construct_dictionary(tree.right, prefix + '1')

    def __getitem__(self, item):
        return self.data[item]