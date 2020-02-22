import zipfile

from rotem_compressor.rotem_compressor import RotemCompressor
from rotem_compressor.unittests.compression_testcase import CompressionTestCase


class RotemCompressionTests(CompressionTestCase):
    compressor = RotemCompressor()

    def test_size_less_than_zip(self):
        rotem_compression = self.compressor.compress(self.data)
        with zipfile.ZipFile('../../test/dickens.zip', 'w', 14) as zfile:
            zfile.writestr('dickens.txt', self.data)
        with open('../../test/dickens.zip', 'rb') as f:
            zip_compression = len(f.read())
        print(zip_compression)
        self.assertLessEqual(len(rotem_compression), zip_compression)
