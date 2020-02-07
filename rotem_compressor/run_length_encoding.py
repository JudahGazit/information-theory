from rotem_compressor.contract.ICompressor import ICompressor


class RunLengthEncoding(ICompressor):
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
        return bytearray(result)

    def decompress(self, compressed):
        result = []
        for i in range(0, len(compressed), 2):
            amount, char = compressed[i], compressed[i + 1]
            result.extend(amount * [char])
        return bytearray(result)