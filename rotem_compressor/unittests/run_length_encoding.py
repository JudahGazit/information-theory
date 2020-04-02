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
        input_data = [12, 'W', 1, 'B', 12, 'W', 3, 'B', 24, 'W', 1, 'B', 14, 'W']
        input_data = bytearray([ord(x) if isinstance(x, str) else x for x in input_data])
        expected_output = 'WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'
        output_data = self.compressor.decompress(input_data)
        self.assertEqual(expected_output, ''.join([chr(x) for x in output_data]))