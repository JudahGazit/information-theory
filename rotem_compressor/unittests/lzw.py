from rotem_compressor.lzw import LZW
from rotem_compressor.unittests.compression_testcase import CompressionTestCase


class LZWTests(CompressionTestCase):
    compressor = LZW(raw_values=True)

    def test_compression_simple(self):
        text = 'aabaaba'
        compressed = self.compressor.compress(bytearray(text, 'ASCII'))
        expected_result = [ord('a'), ord('a'), ord('b'), 256, 258]
        self.assertListEqual(expected_result, compressed)

    def test_decompression_simple(self):
        expected_result = 'aabaaba'
        compressed = [ord('a'), ord('a'), ord('b'), 256, 258]
        decompressed = self.compressor.decompress(compressed)
        self.assertEqual(bytearray(expected_result, 'ASCII'), decompressed)

    def test_compression_decompression_of_reacurring(self):
        text = 'B-u-u-ust B-u-u-ust'
        compressed = self.compressor.compress(bytearray(text, 'ASCII'))
        decompressed = self.compressor.decompress(compressed)
        self.assertEqual(bytearray(text, 'ASCII'), decompressed)