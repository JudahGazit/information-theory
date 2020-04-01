import unittest

from rotem_compressor.utils import from_bytearray


class CompressionTestCase(unittest.TestCase):
    compressor = None
    @classmethod
    def setUpClass(cls):
        with open('../../test/dickens.txt', 'rb') as f:
            cls.data = f.read(3 * 10 ** 6)

    def test_decompression(self):
        if self.compressor:
            compression = self.compressor.compress(self.data)
            decompression = self.compressor.decompress(compression)
            self.assertEqual(self.data.decode(), ''.join(from_bytearray(decompression)))
