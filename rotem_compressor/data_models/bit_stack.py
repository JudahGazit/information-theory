def encode_number(number, width=8):
    return bin(number)[2:].zfill(width)


def encode_array_to_bits(array):
    bit_array = [encode_number(number, 8) for number in array]
    return bit_array


class BitList:
    def __init__(self, array: bytearray):
        self.__array = array
        self.bit_array = ''.join(encode_array_to_bits(array))
        self.current_index = 0

    def append(self, number, width=8):
        self.bit_array += encode_number(number, width)

    def pop(self, width=8):
        if self.current_index < len(self.bit_array):
            popped_bit = self.bit_array[self.current_index:self.current_index + width]
            popped = int(popped_bit, 2)
            self.current_index += width
            return popped

    def __len__(self):
        if self.current_index < len(self.bit_array):
            return len(self.bit_array) - self.current_index
        return 0