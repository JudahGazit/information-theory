import math

from rotem_compressor.contract.ICompressor import ICompressor
from rotem_compressor.data_models.bit_stack import BitStack
from rotem_compressor.utils import *


class LZW(ICompressor):
    initial_dictionary_size = 256

    def __init__(self, maximum_table_size=2 ** 24, raw_values=True):
        """

        :param maximum_table_size: maximal dictionary size to be used in LZW algorithm
        :param raw_values: when True: return all the results encoded as int.
                           when False: encode the results using "variable length" codes.
        """
        self.maximum_table_size = maximum_table_size
        self.raw_values = raw_values

    def __add_code_to_dictionary(self, dictionary, combined_symbols, inv_dict=False):
        if len(dictionary) < self.maximum_table_size:
            if inv_dict:
                dictionary[len(dictionary)] = combined_symbols
            else:
                dictionary[combined_symbols] = len(dictionary)
        
    def __get_code_from_dictionary(self, dictionary, string):
        if self.raw_values:
            return dictionary[string]
        else:
            code_width = math.ceil(math.log2(len(dictionary)))
            return encode_number(dictionary[string], code_width)

    def __code_symbol(self, compressed_data, dictionary, prev_symbols, symbol):
        combined_symbols = prev_symbols + chr(symbol)
        if combined_symbols in dictionary:
            prev_symbols = combined_symbols
        else:
            compressed_value = self.__get_code_from_dictionary(dictionary, prev_symbols)
            compressed_data.append(compressed_value)
            self.__add_code_to_dictionary(dictionary, combined_symbols)
            prev_symbols = chr(symbol)
        return prev_symbols

    def __code_last_symbols_if_necessary(self, compressed_data, dictionary, prev_symbols):
        if prev_symbols in dictionary:
            compressed_value = self.__get_code_from_dictionary(dictionary, prev_symbols)
            compressed_data.append(compressed_value)

    def __encode_result(self, compressed_data):
        if not self.raw_values:
            compressed_data = bits_to_numbers(''.join(compressed_data))
        return compressed_data

    def __decompress_raw(self, compressed, dictionary_inv, dictionary, prev_symbols):
        decompressed = []
        for code in compressed:
            prev_symbols = self.__decode_symbol(code, decompressed, dictionary, dictionary_inv, prev_symbols)
        return decompressed

    def __decompress_bits(self, compressed, dictionary_inv, dictionary, prev_symbols):
        decompressed = []
        stack = BitStack(compressed)
        code_width = 8
        while len(stack) >= code_width:
            if len(decompressed) < self.maximum_table_size - self.initial_dictionary_size:
                code_width = math.ceil(math.log2(2 ** 8 + len(decompressed)))
            code = stack.pop(code_width)
            prev_symbols = self.__decode_symbol(code, decompressed, dictionary, dictionary_inv, prev_symbols)
        return decompressed

    def __decode_symbol(self, code, decompressed, dictionary, dictionary_inv, prev_symbols):
        symbol = dictionary_inv.get(code, prev_symbols + prev_symbols[:1])
        decompressed.append(symbol)
        combined_symbols = prev_symbols + symbol[:1]
        if combined_symbols in dictionary:
            prev_symbols = combined_symbols
        else:
            self.__add_code_to_dictionary(dictionary, combined_symbols)
            self.__add_code_to_dictionary(dictionary_inv, combined_symbols, inv_dict=True)
            prev_symbols = symbol
        return prev_symbols

    def compress(self, data):
        dictionary = {chr(i): i for i in range(self.initial_dictionary_size)}
        prev_symbols = ""
        compressed_data = []
        for symbol in data:
            prev_symbols = self.__code_symbol(compressed_data, dictionary, prev_symbols, symbol)
        self.__code_last_symbols_if_necessary(compressed_data, dictionary, prev_symbols)
        return self.__encode_result(compressed_data)

    def decompress(self, compressed):
        dictionary_inv = {i: chr(i) for i in range(self.initial_dictionary_size)}
        dictionary = {chr(i): i for i in range(self.initial_dictionary_size)}
        prev_symbols = ""
        if self.raw_values:
            decompressed = self.__decompress_raw(compressed, dictionary_inv, dictionary, prev_symbols)
        else:
            decompressed = self.__decompress_bits(compressed, dictionary_inv, dictionary, prev_symbols)
        return to_bytearray(''.join(decompressed))
