from rotem_compressor.contract.ICompressor import ICompressor
import queue

from rotem_compressor.utils import bits_to_numbers, to_bytearray

LEAF_SYMBOL = 1
NONLEAF_SYMBOL = 0


def encode_number(n):
    number_bin = n if isinstance(n, str) else f'{n:b}'
    log_number_bin = f'{len(number_bin):b}'
    prefix = '1' * len(log_number_bin)
    prefix += '0' + log_number_bin
    return prefix + number_bin


def pop_number(bts):
    size = 0
    number_size = ''
    number = ''
    while bts[0] == '1':
        bts.pop(0)
        size += 1
    bts.pop(0)
    for _ in range(size):
        number_size += str(bts.pop(0))
    number_size = int(number_size, 2)
    for _ in range(number_size):
        number += str(bts.pop(0))
    return int(number, 2)


class Huffman(ICompressor):
    def __init__(self, dictionary_size=256):
        self.dictionary_size = dictionary_size

    def compress(self, data):
        result = ''
        root = self.construct_tree(data)
        dictionary = [None] * self.dictionary_size
        self.tree_to_dictionary(dictionary, '', root)
        for char in data:
            result += dictionary[char]
        encode_tree = []
        self.encode_tree(encode_tree, root)
        result_prefix = encode_number(len(data))
        result_prefix += encode_number(len(encode_tree))
        result_prefix += ''.join([encode_number(n or 0) for n in encode_tree])
        result = result_prefix + result
        return bits_to_numbers(result)

    def decompress(self, compressed):
        compressed = list(''.join([bin(x)[2:].zfill(8) for x in compressed]))
        len_data = pop_number(compressed)
        result = []
        dictionary = self.decode_dictionary(compressed)
        inverse_dictionary = {}
        for char, code in enumerate(dictionary):
            inverse_dictionary[code] = char
        char = ''
        compressed = compressed[::-1]
        while len(result) < len_data:
            char += compressed.pop()
            value = inverse_dictionary.get(char)
            if value:
                result.append(value)
                char = ''
        return bytearray(to_bytearray(result))

    def decode_dictionary(self, compressed):
        encode_size = pop_number(compressed)
        encode_tree = []
        for i in range(encode_size):
            encode_tree.append(pop_number(compressed))
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
