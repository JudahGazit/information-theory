from rotem_compressor.contract.ICompressor import ICompressor
import gzip

class RotemCompressor(ICompressor):
    def compress(self, data):
        return gzip.compress(data)

    def decompress(self, compressed):
        return gzip.decompress(compressed)