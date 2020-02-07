import gzip
import unittest

from rotem_compressor.rotem_compressor import RotemCompressor


class RotemCompressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('../../test/dickens.txt', 'rb') as f:
            cls.data = f.read(10000)

    def setUp(self):
        self.rotem_compressor = RotemCompressor()

    def test_decompression(self):
        rotem_compression = self.rotem_compressor.compress(self.data)
        rotem_decompression = self.rotem_compressor.decompress(rotem_compression)
        self.assertEqual(self.data, rotem_decompression)

    def test_size_less_than_zip(self):
        rotem_compression = self.rotem_compressor.compress(self.data)
        zip_compression = gzip.compress(self.data)
        self.assertLessEqual(len(rotem_compression), len(zip_compression))
