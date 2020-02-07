from rotem_compressor.burrows_wheeler_transform import BurrowsWheelerTransform, BEGIN_CHAR, END_CHAR
from rotem_compressor.unittests.compression_testcase import CompressionTestCase


class BurrowsWheelerTransformTests(CompressionTestCase):
    compressor = BurrowsWheelerTransform()
    char_mapping = {BEGIN_CHAR: '^', END_CHAR: '$'}
    char_mapping_inv = {v: k for k, v in char_mapping.items()}

    def test_wikipedia_example_compress(self):
        input_data = 'BANANA'
        expected_output = 'BNN^AA$A'
        output_data = self.compressor.compress(bytes(input_data, 'ASCII'))
        self.assertEqual(expected_output, ''.join([self.char_mapping.get(x, chr(x)) for x in output_data]))

    def test_wikipedia_example_decompress(self):
        input_data = 'BNN^AA$A'
        expected_output = 'BANANA'
        output_data = self.compressor.decompress([self.char_mapping_inv.get(x, ord(x)) for x in input_data])
        self.assertEqual(expected_output, ''.join([self.char_mapping.get(x, chr(x)) for x in output_data]))