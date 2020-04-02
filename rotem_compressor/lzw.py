import math

from rotem_compressor.contract.ICompressor import ICompressor
from rotem_compressor.data_models.bit_stack import BitList
from rotem_compressor.utils import *


class LZW(ICompressor):
    initial_dictionary_size = 256

    def __init__(self, maximum_table_size=2 ** 24, raw_values=True):
        self.maximum_table_size = maximum_table_size
        self.raw_values = raw_values

    def add_code_to_dictionary(self, dictionary, combined_symbols, inv_dict=False):
        if len(dictionary) <= self.maximum_table_size:
            if inv_dict:
                dictionary[len(dictionary)] = combined_symbols
            else:
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

    def decompress_raw(self, compressed, dictionary_inv, dictionary, prev_symbols):
        decompressed = []
        for code in compressed:
            prev_symbols = self.decode_symbol(code, decompressed, dictionary, dictionary_inv, prev_symbols)
        return decompressed

    def decompress_bits(self, compressed, dictionary_inv, dictionary, prev_symbols):
        decompressed = []
        i = 0
        stack = BitList(compressed)
        code_width = 8
        while len(stack) >= code_width:
            code_width = math.ceil(math.log2(2 ** 8 + i))
            code = stack.pop(code_width)
            prev_symbols = self.decode_symbol(code, decompressed, dictionary, dictionary_inv, prev_symbols)
            i += 1
        return decompressed

    def decode_symbol(self, code, decompressed, dictionary, dictionary_inv, prev_symbols):
        symbol = dictionary_inv.get(code, prev_symbols + prev_symbols[:1])
        decompressed.append(symbol)
        combined_symbols = prev_symbols + symbol[:1]
        if combined_symbols in dictionary:
            prev_symbols = combined_symbols
        else:
            self.add_code_to_dictionary(dictionary, combined_symbols)
            self.add_code_to_dictionary(dictionary_inv, combined_symbols, inv_dict=True)
            prev_symbols = symbol
        return prev_symbols

    def decompress(self, compressed):
        dictionary_inv = {i: chr(i) for i in range(self.initial_dictionary_size)}
        dictionary = {chr(i): i for i in range(self.initial_dictionary_size)}
        prev_symbols = ""
        if self.raw_values:
            decompressed = self.decompress_raw(compressed, dictionary_inv, dictionary, prev_symbols)
        else:
            decompressed = self.decompress_bits(compressed, dictionary_inv, dictionary, prev_symbols)
        return to_bytearray(''.join(decompressed))
