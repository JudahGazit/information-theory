from rotem_compressor.run_length_encoding import RunLengthEncoding
from rotem_compressor.unittests.compression_testcase import CompressionTestCase


class RunLengthEncodingTests(CompressionTestCase):
    compressor = RunLengthEncoding(threshold=2)
    def test_wikipedia_example_compress(self):
        input_data = 'WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'
        expected_output = ['W', 'W', 12, 'B', 'W', 'W', 12, 'B', 'B', 3, 'W', 'W', 24,  'B', 'W', 'W', 14]
        expected_output = bytearray([ord(x) if isinstance(x, str) else x for x in expected_output])
        output_data = self.compressor.compress(bytes(input_data, 'ASCII'))
        self.assertEqual(expected_output, output_data)

    def test_wikipedia_example_decompress(self):
        input_data = ['W', 'W', 12, 'B', 'W', 'W', 12, 'B', 'B', 3, 'W', 'W', 24,  'B', 'W', 'W', 14]
        input_data = bytearray([ord(x) if isinstance(x, str) else x for x in input_data])
        expected_output = 'WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'
        output_data = self.compressor.decompress(input_data)
        self.assertEqual(expected_output, ''.join([chr(x) for x in output_data]))

    def test_wikipedia_example(self):
        input_data = 'WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'
        input_data_bin = bytearray([ord(x) if isinstance(x, str) else x for x in input_data])
        output_data = self.compressor.compress(input_data_bin)
        output_data = self.compressor.decompress(output_data)
        self.assertEqual(input_data, ''.join([chr(x) for x in output_data]))