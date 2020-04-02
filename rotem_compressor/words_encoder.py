import re
import math
from rotem_compressor.contract.ICompressor import ICompressor
from rotem_compressor.data_models.bit_stack import BitStack
from rotem_compressor.huffman_compression.huffman_compression import Huffman
from rotem_compressor.utils import to_bytearray

NEW_LINE = '\n'
SPACE = ' '
SPACES = ''.join([NEW_LINE, SPACE])
DELIMITERS = '.,;:\'"?!(){}\[\]&#/_\{\}*`-'


class WordsEncoder(ICompressor):
    def __replace_words_with_indexes(self, data, words):
        words = {w: i + 1 for i, w in enumerate(words)}
        result = self.__split_text_to_words_and_delimiters(data)
        result = [words[w] for w in result]
        return result

    def __split_text_to_words_and_delimiters(self, data):
        result = []
        word = ''
        for char in data:
            if char not in SPACES + DELIMITERS:
                word += char
            else:
                result.extend([word, char])
                word = ''
        if word != '':
            result.append(word)
        return result

    def __distinct_words_from_data(self, data):
        words = []
        rows = data.split(NEW_LINE)
        for row in rows:
            words.extend(re.sub(f'[{DELIMITERS}]', SPACE, row).split(SPACE))
        words = list(set(words))
        words = list(SPACES + DELIMITERS) + words
        return words

    def __decode_words(self, compressed, length):
        words = []
        for i in range(length):
            words.append(compressed.pop())
        words = Huffman().decompress(words)
        words = ''.join(map(chr, words)).split('\0')
        return words

    def __compress_payload(self, data, words):
        huffman = Huffman(2 ** math.ceil(math.log2(len(words)))).compress(data)
        words_prefix = '\0'.join(words)
        huffman_prefix = Huffman().compress(bytearray(map(ord, words_prefix)))
        compressed = BitStack([])
        compressed.append_natural_number(len(huffman_prefix))
        compressed += BitStack(huffman_prefix)
        compressed += BitStack(huffman)
        return compressed.to_numbers()

    def __decompress_payload(self, compressed, words):
        compressed.bit_array = compressed.bit_array[compressed.current_index:]
        huffman = Huffman(2 ** math.ceil(math.log2(len(words))))
        decompressed = huffman.decompress(compressed.to_numbers())
        decompressed = [words[code - 1] for code in decompressed]
        return decompressed

    def compress(self, data):
        data = ''.join(map(chr, data))
        words = self.__distinct_words_from_data(data)
        data = self.__replace_words_with_indexes(data, words)
        compressed = self.__compress_payload(data, words)
        return compressed

    def decompress(self, compressed):
        compressed = BitStack(compressed)
        word_amount = compressed.pop_natural_number()
        words = self.__decode_words(compressed, word_amount)
        decompressed = self.__decompress_payload(compressed, words)
        return to_bytearray(''.join(decompressed))
