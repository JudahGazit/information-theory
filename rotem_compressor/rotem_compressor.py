from rotem_compressor.contract.ICompressor import ICompressor

from rotem_compressor.huffman_compression.huffman_compression import Huffman
from rotem_compressor.lzw import LZW
from rotem_compressor.words_encoder import WordsEncoder


class RotemCompressor(ICompressor):
    compressions = [
        LZW(2 ** 20, raw_values=False),
    ]
    # compressions = [
    #     LZW(2 ** 20, raw_values=True),
    #     # Huffman?(2 ** 16),
    # ]
    # compressions = [
    #     WordsEncoder()
    # ]

    def compress(self, data):
        for compression in self.compressions:
            data = compression.compress(data)
        return data

    def decompress(self, compressed):
        for compression in self.compressions[::-1]:
            compressed = compression.decompress(compressed)
        return compressed
