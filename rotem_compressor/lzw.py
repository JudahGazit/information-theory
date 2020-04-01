import math

from rotem_compressor.contract.ICompressor import ICompressor
from rotem_compressor.utils import *


class LZW(ICompressor):
    def __init__(self, maximum_table_size=2 ** 24, return_raw_results=True):
        self.maximum_table_size = maximum_table_size
        self.raw_values = return_raw_results

    def compress(self, data):
        dictionary_size = 256
        dictionary = {chr(i): i for i in range(dictionary_size)}
        string = ""
        compressed_data = []
        for symbol in data:
            string_plus_symbol = string + chr(symbol)
            if string_plus_symbol in dictionary:
                string = string_plus_symbol
            else:
                compressed_value = dictionary[string] if self.raw_values else encode_number(dictionary[string], math.ceil(math.log2(dictionary_size)))
                compressed_data.append(compressed_value)
                if len(dictionary) <= self.maximum_table_size:
                    dictionary[string_plus_symbol] = dictionary_size
                    dictionary_size += 1
                string = chr(symbol)

        if string in dictionary:
            compressed_value = dictionary[string] if self.raw_values else encode_number(dictionary[string], math.ceil(math.log2(dictionary_size)))
            compressed_data.append(compressed_value)
        if not self.raw_values:
            compressed_data = bits_to_numbers(''.join(compressed_data))
        return compressed_data

    def decompress(self, compressed):
        decompresed = []
        dictionary_size = 256
        dictionary_inv = {i: chr(i) for i in range(dictionary_size)}
        dictionary = {chr(i): i for i in range(dictionary_size)}
        string = ""  # String is null.
        i = 0
        while len(compressed):
            try:
                i += 1
                c, compressed = compressed[0], compressed[1:] if self.raw_values else pop_number(compressed, math.ceil(math.log2(dictionary_size)))
                symbol = dictionary_inv.get(c, string + string[:1])
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
            except:
                raise
        return to_bytearray(''.join(decompresed))
