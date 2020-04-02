def encode_number(number, width=8):
    return bin(number)[2:].zfill(width)


def encode_array_to_bits(array):
    bit_array = [encode_number(number, 8) for number in array]
    return bit_array


class BitStack:
    def __init__(self, array: bytearray):
        self.__array = array
        self.bit_array = ''.join(encode_array_to_bits(array))
        self.bit_array = list(self.bit_array)
        self.current_index = 0

    def append(self, number, width=8):
        self.bit_array += encode_number(number, width)

    def append_natural_number(self, number):
        pass

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
            char = self.bit_array[self.current_index : index]
            value = dictionary.get(''.join(char))
        self.current_index = index
        return value

    def __iter__(self):
        return self.bit_array.copy()

    def __len__(self):
        if self.current_index < len(self.bit_array):
            return len(self.bit_array) - self.current_index
        return 0