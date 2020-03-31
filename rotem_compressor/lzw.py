import math

from rotem_compressor.contract.ICompressor import ICompressor
from rotem_compressor.utils import *


class LZW(ICompressor):
    maximum_table_size = pow(2, int(12))

    def compress(self, data):
        dictionary_size = 256
        dictionary = {chr(i): i for i in range(dictionary_size)}
        string = ""
        compressed_data = ""
        for symbol in data:
            string_plus_symbol = string + chr(symbol)
            if string_plus_symbol in dictionary:
                string = string_plus_symbol
            else:
                compressed_data += encode_number(dictionary[string], math.ceil(math.log2(dictionary_size)))
                if len(dictionary) <= self.maximum_table_size:
                    dictionary[string_plus_symbol] = dictionary_size
                    dictionary_size += 1
                string = chr(symbol)

        if string in dictionary:
            compressed_data += encode_number(dictionary[string], math.ceil(math.log2(dictionary_size)))
        return bits_to_numbers(compressed_data)



    def decompress(self, compressed):
        decompresed = []
        dictionary_size = 256
        dictionary_inv = {i: chr(i) for i in range(dictionary_size)}
        dictionary = {chr(i): i for i in range(dictionary_size)}
        string = ""  # String is null.
        while len(compressed):
            c, compressed = pop_number(compressed, math.ceil(math.log2(dictionary_size)))
            symbol = dictionary_inv[c]
            decompresed.append(symbol)
            string_plus_symbol = string + symbol[:1]  # get input symbol.
            if string_plus_symbol in dictionary:
                string = string_plus_symbol
            else:
                if len(dictionary) <= self.maximum_table_size:
                    dictionary[string_plus_symbol] = dictionary_size
                    dictionary_inv[dictionary_size] = string_plus_symbol
                    dictionary_size += 1
                string = symbol
        return to_bytearray(''.join(decompresed))