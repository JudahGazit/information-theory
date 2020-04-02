import zipfile

from rotem_compressor.rotem_compressor import RotemCompressor
from rotem_compressor.unittests.compression_testcase import CompressionTestCase


class RotemCompressionTests(CompressionTestCase):
    compressor = RotemCompressor()

    def test_size_less_than_zip(self):
        rotem_compression = self.compressor.compress(self.data)
        with zipfile.ZipFile('../../test/dickens.zip', 'w', 14, False) as zfile:
            zfile.writestr('dickens.txt', self.data)
        with open('../../test/dickens.zip', 'rb') as f:
            data = f.read()
            zip_compression = len(data)
        print(f'zip: {zip_compression}, rotem:{len(rotem_compression)}')
        self.assertLessEqual(len(rotem_compression), zip_compression)
