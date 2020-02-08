import unittest


class CompressionTestCase(unittest.TestCase):
    compressor = None
    @classmethod
    def setUpClass(cls):
        with open('../../test/dickens.txt', 'rb') as f:
            cls.data = f.read(10000)

    def test_decompression(self):
        if self.compressor:
            compression = self.compressor.compress(self.data)
            decompression = self.compressor.decompress(compression)
            self.assertEqual(self.data, decompression)
