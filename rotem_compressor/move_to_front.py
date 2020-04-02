from rotem_compressor.contract.ICompressor import ICompressor
from rotem_compressor.utils import to_bytearray

ZERO_ALIAS = 254

class MoveToFront(ICompressor):
    def __init__(self, dictionary=None):
        self.dictionary = dictionary or list(range(256))

    def compress(self, data):
        dictionary = self.dictionary.copy()
        result = []
        zero_counter = 0
        last_zero = False
        for char in data:
            index = dictionary.index(char)
            if index == 0:
                zero_counter += 1
                last_zero = True
            elif last_zero:
                last_zero = False
                result.append(ZERO_ALIAS)
                result.append(zero_counter)
                result.append(index)
                zero_counter = 0
            else:
                result.append(index)
            dictionary.pop(index)
            dictionary.insert(0, char)
        if last_zero:
            result.append(ZERO_ALIAS)
            result.append(zero_counter)
        return bytearray(result)

    def decompress(self, compressed):
        dictionary = self.dictionary.copy()
        result = []
        last_zero = False
        for i, index in enumerate(compressed):
            index = index if index != ZERO_ALIAS else 0
            char = dictionary[index]
            if index == 0:
                last_zero = True
                result.extend([char] * compressed[i + 1])
            elif not last_zero:
                result.append(char)
            else:
                last_zero = False
                continue
            dictionary.pop(index)
            dictionary.insert(0, char)
        return to_bytearray(result)