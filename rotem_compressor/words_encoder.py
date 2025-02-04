import re
import math
from rotem_compressor.contract.ICompressor import ICompressor
from rotem_compressor.data_models.bit_stack import BitStack
from rotem_compressor.huffman_compression.huffman_compression import Huffman
from rotem_compressor.lzw import LZW
from rotem_compressor.utils import to_bytearray

DELIMITERS = '.,;:\'"?!(){}\[\]&#/_\{\}*`@~<>\\+ \n-'


class WordsEncoder(ICompressor):
    def __init__(self, maximum_table_size=2 ** 14):
        self.maximum_table_size = maximum_table_size
        self.lzw_compressor = LZW(self.maximum_table_size, raw_values=False)

    def __replace_words_with_indexes(self, data, words):
        words = {w: i + 1 for i, w in enumerate(words)}
        result = self.__split_text_to_words_and_delimiters(data)
        result = [words[w] for w in result]
        return result

    def __split_text_to_words_and_delimiters(self, data):
        result = []
        word = ''
        for char in data:
            word = self.__append_to_result_if_end_of_word(char, result, word)
        if word != '':
            result.append(word)
        return result

    def __append_to_result_if_end_of_word(self, char, result, word):
        if char not in DELIMITERS:
            word += char
        else:
            if word != '':
                result.append(word)
            result.append(char)
            word = ''
        return word

    def __distinct_words_from_data(self, data):
        words = re.sub(f'[{DELIMITERS}]+', ' ', data).split(' ')
        words = list(set(words))
        words = list(DELIMITERS) + words
        return words

    def __decode_words(self, compressed, length):
        words = []
        for i in range(length):
            words.append(compressed.pop())
        decompressed_words = self.lzw_compressor.decompress(words)
        decompressed_words = ''.join(map(chr, decompressed_words)).split('\0')
        return decompressed_words

    def __compress_payload(self, data, words):
        huffman = Huffman(len(words) + 1).compress(data)
        words_prefix = '\0'.join(words)
        compressed_prefix = self.lzw_compressor.compress(bytearray(map(ord, words_prefix)))
        compressed = BitStack([])
        compressed.append_natural_number(len(compressed_prefix))
        compressed += BitStack(compressed_prefix)
        compressed += BitStack(huffman)
        return compressed.to_numbers()

    def __decompress_payload(self, compressed, words):
        compressed.bit_array = compressed.bit_array[compressed.current_index:]
        huffman = Huffman(len(words) + 1)
        decompressed = huffman.decompress(compressed.to_numbers())
        return decompressed

    def __replace_indexes_to_words(self, decompressed, words):
        decompressed = [words[code - 1] for code in decompressed]
        decompressed = ''.join(decompressed)
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
        decompressed = self.__replace_indexes_to_words(decompressed, words)
        return to_bytearray(decompressed)
