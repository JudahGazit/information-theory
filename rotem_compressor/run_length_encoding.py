from rotem_compressor.contract.ICompressor import ICompressor
from rotem_compressor.utils import to_bytearray


class RunLengthEncoding(ICompressor):
    def __init__(self, threshold):
        self.threshold = threshold

    def compress(self, data):
        result = []
        last_char = None
        char_counter = 0
        for char in data:
            if char == last_char or last_char is None:
                last_char = char
                char_counter += 1
            else:
                result.append(char_counter)
                result.append(last_char)
                last_char = char
                char_counter = 1
        result.append(char_counter)
        result.append(last_char)
        return self.represent_result(result)

    def represent_result(self, compressed):
        result = []
        for i in range(0, len(compressed), 2):
            amount, char = compressed[i], compressed[i + 1]
            if amount >= self.threshold:
                result.extend(self.threshold * [char])
                result.append(amount)
            else:
                result.extend(amount * [char])
        return to_bytearray(result)

    def decompress(self, compressed):
        result = []
        last_char = None
        char_counter = 0
        for char in compressed:
            if last_char is None:
                last_char = char
            if char == last_char:
                char_counter += 1
            else:
                if char_counter == self.threshold:
                    result.extend(int(char) * [last_char])
                    last_char = None
                    char_counter = 0
                else:
                    result.extend(char_counter * [last_char])
                    last_char = char
                    char_counter = 1
        if last_char:
            result.extend(char_counter * [last_char])
        return to_bytearray(result)

