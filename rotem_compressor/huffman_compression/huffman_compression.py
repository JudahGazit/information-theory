import queue

from rotem_compressor.contract.ICompressor import ICompressor
from rotem_compressor.data_models.bit_stack import BitStack
from rotem_compressor.huffman_compression.graph_node import Node, NONLEAF_SYMBOL, LEAF_SYMBOL
from rotem_compressor.utils import bits_to_numbers, to_bytearray


class Huffman(ICompressor):
    def __init__(self, dictionary_size=256):
        self.dictionary_size = dictionary_size

    def compress(self, data):
        payload = ''
        root = self.construct_tree(data)
        dictionary = [None] * self.dictionary_size
        self.tree_to_dictionary(dictionary, '', root)
        for char in data:
            payload += dictionary[char]
        result = self.__build_result(data, root, payload)
        return result

    def __build_result(self, data, root, payload):
        bit_stack = BitStack([])
        encode_tree = []
        self.encode_tree(encode_tree, root)
        bit_stack.append_natural_number(len(data))
        bit_stack.append_natural_number(len(encode_tree))
        for n in encode_tree:
            bit_stack.append_natural_number(n or 0)
        bit_stack.concat(list(payload))
        return bit_stack.to_numbers()

    def decompress(self, compressed):
        result = []
        compressed = BitStack(compressed)
        data_length = compressed.pop_natural_number()
        dictionary = self.decode_dictionary(compressed)
        inverse_dictionary = {code: char for char, code in enumerate(dictionary)}
        while len(result) < data_length and len(compressed) > 0:
            popped = compressed.pop_prefix_code(inverse_dictionary)
            result.append(popped)
        return to_bytearray(result)

    def decode_dictionary(self, compressed):
        encode_size = compressed.pop_natural_number()
        encode_tree = []
        for i in range(encode_size):
            encode_tree.append(compressed.pop_natural_number())
        encode_tree.pop(0)
        decode_tree = Node(None, None, None)
        self.decode_tree(encode_tree, decode_tree)
        dictionary = [None] * self.dictionary_size
        self.tree_to_dictionary(dictionary, '', decode_tree)
        return dictionary

    def encode_tree(self, encode, tree):
        if tree:
            if tree.left is None and tree.right is None:
                encode.append(LEAF_SYMBOL)
                encode.append(tree.data)
            else:
                encode.append(NONLEAF_SYMBOL)
            self.encode_tree(encode, tree.left)
            self.encode_tree(encode, tree.right)

    def decode_tree(self, encode, tree):
        if tree.left is None and len(encode):
            current, new_node = self.decode_node(encode)
            tree.left = new_node
            if current == NONLEAF_SYMBOL:
                self.decode_tree(encode, tree.left)
        if tree.right is None and len(encode):
            current, new_node = self.decode_node(encode)
            tree.right = new_node
            if current == NONLEAF_SYMBOL:
                self.decode_tree(encode, tree.right)

    def decode_node(self, encode):
        current = encode.pop(0)
        if current == NONLEAF_SYMBOL:
            new_node = Node(None, None, None)
        else:
            new_node = Node(None, None, encode.pop(0))
        return current, new_node

    def get_frequencies(self, data):
        frequencies = [0] * self.dictionary_size
        for char in data:
            frequencies[char] += 1
        return frequencies

    def construct_tree(self, data):
        frequencies = self.get_frequencies(data)
        priority_queue = queue.PriorityQueue()
        for char, frequency in enumerate(frequencies):
            if frequency > 0:
                priority_queue.put((frequency, Node(None, None, char)))
        while priority_queue.qsize() > 1:
            left_frequency, left = priority_queue.get()
            right_frequency, right = priority_queue.get()
            priority_queue.put((left_frequency + right_frequency, Node(left, right, None)))
        return priority_queue.get()[1]

    def tree_to_dictionary(self, dictionary, prefix, tree):
        if tree:
            if tree.left is None and tree.right is None:
                dictionary[tree.data] = prefix
            self.tree_to_dictionary(dictionary, prefix + '0', tree.left)
            self.tree_to_dictionary(dictionary, prefix + '1', tree.right)