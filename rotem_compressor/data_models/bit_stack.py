from rotem_compressor.utils import encode_number, bits_to_numbers


def encode_array_to_bits(array):
    bit_array = [encode_number(number, 8) for number in array]
    return bit_array


def number_prefix_code(n):
    number_bin = n if isinstance(n, str) else f'{n:b}'
    log_number_bin = f'{len(number_bin):b}'
    prefix = '1' * len(log_number_bin)
    prefix += '0' + log_number_bin
    return prefix + number_bin


class BitStack:
    def __init__(self, array=None, bit_array=None):
        self.__array = array
        self.bit_array = bit_array or ''.join(encode_array_to_bits(array))
        self.bit_array = list(self.bit_array)
        self.current_index = 0

    def append(self, number, width=8):
        self.bit_array.extend(encode_number(number, width))

    def append_natural_number(self, number):
        self.bit_array.extend(number_prefix_code(number))

    def concat(self, bit_array):
        self.bit_array += bit_array

    def __add__(self, other):
        if isinstance(other, BitStack):
            new_bitstack = BitStack(bit_array=self.bit_array + other.bit_array)
            return new_bitstack

    def pop(self, width=8):
        if self.current_index < len(self.bit_array):
            popped_bit = self.bit_array[self.current_index:self.current_index + width]
            popped = int(''.join(popped_bit), 2)
            self.current_index += width
            return popped

    def pop_natural_number(self):
        size = 0
        while self.bit_array[self.current_index] == '1':
            self.current_index += 1
            size += 1
        self.current_index += 1
        number_size = self.pop(size)
        number = self.pop(number_size)
        return number

    def pop_prefix_code(self, dictionary):
        value = None
        index = self.current_index
        while index < len(self.bit_array) and value is None:
            index += 1
            char = self.bit_array[self.current_index: index]
            value = dictionary.get(''.join(char))
        self.current_index = index
        return value

    def to_numbers(self):
        return bits_to_numbers(''.join(self.bit_array))

    def __iter__(self):
        for bit in self.bit_array:
            yield bit

    def __len__(self):
        if self.current_index < len(self.bit_array):
            return len(self.bit_array) - self.current_index
        return 0
