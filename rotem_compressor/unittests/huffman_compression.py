from rotem_compressor.data_models.tree_node import Node
from rotem_compressor.huffman_compression.dictionary import Dictionary
from rotem_compressor.huffman_compression.huffman_compression import Huffman
from rotem_compressor.unittests.compression_testcase import CompressionTestCase


class HuffmanTests(CompressionTestCase):
    compressor = Huffman()

    def test_get_frequencies(self):
        data = 'hello world'
        data = bytearray(data, 'ASCII')
        frequencies = self.compressor.tree_builder.get_frequencies(data)
        self.assertEqual(frequencies[ord('l')], 3)
        self.assertEqual(frequencies[ord('e')], 1)
        self.assertEqual(frequencies[ord(' ')], 1)
        self.assertEqual(frequencies[ord('a')], 0)

    def test_construct_tree(self):
        data = 'this is an example of a huffman tree'
        data = bytearray(data, 'ASCII')
        tree = self.compressor.tree_builder.construct_tree(data)
        # Asserting by the image from wikipedia:
        # https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Huffman_tree_2.svg/675px-Huffman_tree_2.svg.png
        dictionary = Dictionary(256, tree)
        self.assertLessEqual(len(dictionary[ord("e")]), 3)
        self.assertLessEqual(len(dictionary[ord("a")]), 3)
        self.assertLessEqual(len(dictionary[ord(" ")]), 3)
        self.assertLessEqual(len(dictionary[ord("o")]), 5)

    def test_encode_decode_tree(self):
        data = 'this is an example of a huffman tree'
        data = bytearray(data, 'ASCII')
        tree = self.compressor.tree_builder.construct_tree(data)
        encode = self.compressor.tree_encoder.encode_tree(tree)
        encode.pop(0)
        decode_tree = Node(None, None, None)
        self.compressor.tree_encoder.construct_tree_from_list(encode, decode_tree)
        dictionary_original = Dictionary(256, tree)
        dictionary_decode = Dictionary(256, decode_tree)
        self.assertListEqual(dictionary_original.data, dictionary_decode.data)

    def test_encode_tree(self):
        root = Node(Node(Node(None, None, 71), Node(None, None, 72), None), None, None)
        root.print_tree(0)
        encode = self.compressor.tree_encoder.encode_tree(root)
        self.assertListEqual(encode, [0, 0, 1, 71, 1, 72])

    def test_decode_tree(self):
        encoded = [0, 0, 1, 71, 1, 72]
        root = Node(None, None, None)
        encoded.pop(0)
        self.compressor.tree_encoder.construct_tree_from_list(encoded, root)
        root.print_tree(0)
        self.assertEqual(root.left.left.data, 71)
        self.assertEqual(root.left.right.data, 72)
        self.assertIsNone(root.right)
