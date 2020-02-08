from rotem_compressor.move_to_front import MoveToFront, ZERO_ALIAS
from rotem_compressor.unittests.compression_testcase import CompressionTestCase


class RunLengthEncodingTests(CompressionTestCase):
    compressor = MoveToFront()
    def test_wikipedia_example_compress(self):
        dictionary = 'abcdefghijklmnopqrstuvwxyz'
        compressor = MoveToFront(dictionary=[ord(x) for x in dictionary])
        input_data = 'bananaaaaaaaaaa'
        expected_output = bytearray([1, 1, 13, 1, 1, 1, ZERO_ALIAS, 9])
        output_data = compressor.compress(bytes(input_data, 'ASCII'))
        self.assertEqual(expected_output, output_data)

    def test_wikipedia_example_decompress(self):
        dictionary = 'abcdefghijklmnopqrstuvwxyz'
        compressor = MoveToFront(dictionary=[ord(x) for x in dictionary])
        input_data = bytearray([1, 1, 13, 1, 1, 1, ZERO_ALIAS, 2])
        expected_output = 'bananaaa'
        output_data = compressor.decompress(input_data)
        self.assertEqual(expected_output, ''.join([chr(x) for x in output_data]))