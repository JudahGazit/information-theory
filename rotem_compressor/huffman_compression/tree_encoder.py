from rotem_compressor.data_models.tree_node import LEAF_SYMBOL, NONLEAF_SYMBOL, Node


def decode_node(encode):
    current = encode.pop(0)
    if current == NONLEAF_SYMBOL:
        new_node = Node(None, None, None)
    else:
        new_node = Node(None, None, encode.pop(0))
    return current, new_node


class TreeEncoder:
    def _encode_tree_recursive(self, encode, tree):
        if tree:
            if tree.left is None and tree.right is None:
                encode.append(LEAF_SYMBOL)
                encode.append(tree.data)
            else:
                encode.append(NONLEAF_SYMBOL)
            self._encode_tree_recursive(encode, tree.left)
            self._encode_tree_recursive(encode, tree.right)

    def encode_tree(self, tree):
        encode = []
        self._encode_tree_recursive(encode, tree)
        return encode

    def __read_encoded_tree(self, bit_stack):
        encode_size = bit_stack.pop_natural_number()
        encode_tree = []
        for i in range(encode_size):
            encode_tree.append(bit_stack.pop_natural_number())
        encode_tree.pop(0)
        return encode_tree

    def _construct_tree_from_list(self, encode, tree):
        if tree.left is None and len(encode):
            current, new_node = decode_node(encode)
            tree.left = new_node
            if current == NONLEAF_SYMBOL:
                self._construct_tree_from_list(encode, tree.left)
        if tree.right is None and len(encode):
            current, new_node = decode_node(encode)
            tree.right = new_node
            if current == NONLEAF_SYMBOL:
                self._construct_tree_from_list(encode, tree.right)

    def decode_tree(self, bit_stack):
        encode_tree = self.__read_encoded_tree(bit_stack)
        decode_tree = Node(None, None, None)
        self._construct_tree_from_list(encode_tree, decode_tree)
        return decode_tree

