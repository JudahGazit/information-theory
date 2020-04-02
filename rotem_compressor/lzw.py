import math

from rotem_compressor.contract.ICompressor import ICompressor
from rotem_compressor.data_models.bit_stack import BitList
from rotem_compressor.utils import *


class LZW(ICompressor):
    initial_dictionary_size = 256

    def __init__(self, maximum_table_size=2 ** 24, raw_values=True):
        self.maximum_table_size = maximum_table_size
        self.raw_values = raw_values

    def add_code_to_dictionary(self, dictionary, combined_symbols):
        if len(dictionary) <= self.maximum_table_size:
            dictionary[combined_symbols] = len(dictionary)
        
    def get_code_from_dictionary(self, dictionary, string):
        if self.raw_values:
            return dictionary[string]
        else:
            code_width = math.ceil(math.log2(len(dictionary)))
            return encode_number(dictionary[string], code_width)

    def code_symbol(self, compressed_data, dictionary, prev_symbols, symbol):
        combined_symbols = prev_symbols + chr(symbol)
        if combined_symbols in dictionary:
            prev_symbols = combined_symbols
        else:
            compressed_value = self.get_code_from_dictionary(dictionary, prev_symbols)
            compressed_data.append(compressed_value)
            self.add_code_to_dictionary(dictionary, combined_symbols)
            prev_symbols = chr(symbol)
        return prev_symbols

    def code_last_symbols_if_necessary(self, compressed_data, dictionary, prev_symbols):
        if prev_symbols in dictionary:
            compressed_value = self.get_code_from_dictionary(dictionary, prev_symbols)
            compressed_data.append(compressed_value)

    def encode_result(self, compressed_data):
        if not self.raw_values:
            compressed_data = bits_to_numbers(''.join(compressed_data))
        return compressed_data

    def compress(self, data):
        dictionary = {chr(i): i for i in range(self.initial_dictionary_size)}
        prev_symbols = ""
        compressed_data = []
        for symbol in data:
            prev_symbols = self.code_symbol(compressed_data, dictionary, prev_symbols, symbol)
        self.code_last_symbols_if_necessary(compressed_data, dictionary, prev_symbols)
        return self.encode_result(compressed_data)

    def decompress(self, compressed):
        decompresed = []
        dictionary_size = self.initial_dictionary_size
        dictionary_inv = {i: chr(i) for i in range(dictionary_size)}
        dictionary = {chr(i): i for i in range(dictionary_size)}
        string = ""  # String is null.
        i = 0
        stack = compressed[::-1] if self.raw_values else BitList(compressed)
        code_width = 8
        while (not self.raw_values and len(stack) >= code_width) or (self.raw_values and len(stack) > 0):
            i += 1
            code_width = math.ceil(math.log2(2 ** 8 + i - 1))
            c = stack.pop() if self.raw_values else stack.pop(code_width)
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
        return to_bytearray(''.join(decompresed))
