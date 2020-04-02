from rotem_compressor.burrows_wheeler_transform import BurrowsWheelerTransform
from rotem_compressor.contract.ICompressor import ICompressor

from rotem_compressor.huffman_compression import Huffman
from rotem_compressor.lzw import LZW
from rotem_compressor.move_to_front import MoveToFront
from rotem_compressor.run_length_encoding import RunLengthEncoding
from rotem_compressor.utils import from_bytearray


class RotemCompressor(ICompressor):
    compressions = [LZW(raw_values=False)]

    def compress(self, data):
        for compression in self.compressions:
            data = compression.compress(data)
        return data

    def decompress(self, compressed):
        for compression in self.compressions[::-1]:
            compressed = compression.decompress(compressed)
        return compressed