from rotem_compressor.contract.ICompressor import ICompressor

from rotem_compressor.huffman_compression.huffman_compression import Huffman
from rotem_compressor.lzw import LZW


class RotemCompressor(ICompressor):
    compressions = [LZW(2 ** 12, raw_values=True), Huffman(2 ** 12)]

    def compress(self, data):
        for compression in self.compressions:
            data = compression.compress(data)
        return data

    def decompress(self, compressed):
        for compression in self.compressions[::-1]:
            compressed = compression.decompress(compressed)
        return compressed