import gzip
import unittest

from rotem_compressor.rotem_compressor import RotemCompressor
from rotem_compressor.unittests.compression_testcase import CompressionTestCase


class RotemCompressionTests(CompressionTestCase):
    compressor = RotemCompressor()

    @classmethod
    def setUpClass(cls):
        with open('../../test/dickens.txt', 'rb') as f:
            cls.data = f.read(10000)

    def test_size_less_than_zip(self):
        rotem_compression = self.compressor.compress(self.data)
        zip_compression = gzip.compress(self.data)
        self.assertLessEqual(len(rotem_compression), len(zip_compression))
