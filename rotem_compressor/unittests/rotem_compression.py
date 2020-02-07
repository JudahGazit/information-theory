import gzip
import unittest

from rotem_compressor.rotem_compressor import RotemCompressor
from rotem_compressor.unittests.compression_testcase import CompressionTestCase


class RotemCompressionTests(CompressionTestCase):
    compressor = RotemCompressor()

    def test_size_less_than_zip(self):
        rotem_compression = self.compressor.compress(self.data)
        zip_compression = gzip.compress(self.data)
        self.assertLessEqual(len(rotem_compression), len(zip_compression))
