from pprint import pprint

from rotem_compressor.contract.ICompressor import ICompressor

BEGIN_CHAR = 0
END_CHAR = 255
CHUNK_SIZE = 100


class BurrowsWheelerTransform(ICompressor):
    def __init__(self, chunk_size=CHUNK_SIZE):
        self.chunk_size = chunk_size

    def chunk(self, data, n):
        for i in range(0, len(data), n):
            yield data[i:i + n]

    def compress(self, data):
        result = []
        for chunk in self.chunk(data, self.chunk_size):
            result.extend(self.compress_chunk(chunk))
        return bytearray(result)

    def decompress(self, compressed):
        result = []
        for chunk in self.chunk(compressed, self.chunk_size + 2):
            result.extend(self.decompress_chunk(chunk))
        return bytearray(result)

    def compress_chunk(self, data):
        data = list(data)
        data.insert(0, BEGIN_CHAR)
        data.append(END_CHAR)
        data_permutations = []
        for i in range(len(data)):
            data_permutations.append(data[i:] + data[:i])
        data_permutations.sort()
        return [permutation[-1] for permutation in data_permutations]

    def decompress_chunk(self, compressed):
        result = [[x] for x in compressed]
        for i in range(len(compressed) - 1):
            result.sort()
            result = [[x] + l for l, x in zip(result, compressed)]
        for row in result:
            if row[-1] == END_CHAR:
                return row[1:-1]
