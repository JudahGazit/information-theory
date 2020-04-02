from rotem_compressor.contract.ICompressor import ICompressor
from rotem_compressor.data_models.bit_stack import BitStack
from rotem_compressor.huffman_compression.dictionary import Dictionary
from rotem_compressor.huffman_compression.tree_builder import TreeBuilder
from rotem_compressor.huffman_compression.tree_encoder import TreeEncoder
from rotem_compressor.utils import to_bytearray


class Huffman(ICompressor):
    def __init__(self, dictionary_size=256):
        self.dictionary_size = dictionary_size
        self.tree_encoder = TreeEncoder()
        self.tree_builder = TreeBuilder(dictionary_size)

    def __build_result(self, data, root, payload):
        bit_stack = BitStack([])
        encode_tree = self.tree_encoder.encode_tree(root)
        bit_stack.append_natural_number(len(data))
        bit_stack.append_natural_number(len(encode_tree))
        for n in encode_tree:
            bit_stack.append_natural_number(n or 0)
        bit_stack.concat(list(payload))
        return bit_stack.to_numbers()

    def compress(self, data):
        payload = ''
        root = self.tree_builder.construct_tree(data)
        dictionary = Dictionary(self.dictionary_size, root)
        for char in data:
            payload += dictionary[char]
        result = self.__build_result(data, root, payload)
        return result

    def decompress(self, stack):
        result = []
        stack = BitStack(stack)
        data_length = stack.pop_natural_number()
        root = self.tree_encoder.decode_tree(stack)
        dictionary = Dictionary(self.dictionary_size, root)
        inverse_dictionary = {code: char for char, code in enumerate(dictionary)}
        while len(result) < data_length and len(stack) > 0:
            popped = stack.pop_prefix_code(inverse_dictionary)
            result.append(popped)
        return to_bytearray(result)

