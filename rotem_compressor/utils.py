def to_bytearray(values):
    byte_array = []
    max_int = 0
    if isinstance(values, bytearray):
        return values
    for item in values:
        if isinstance(item, str):
            for c in item:
                byte_array.append(ord(c))
                max_int = max_int if max_int > ord(c) else ord(c)
        else:
            byte_array.append(item)
            max_int = max_int if max_int > item else item
    if max_int > 256:
        return byte_array
    return bytearray(byte_array)


def bits_to_numbers(bits):
    result = []
    for index in range(0, len(bits), 8):
        bit = bits[index:index + 8]
        bit = ''.join(bit)
        bit = bit[::-1].zfill(8)[::-1]
        bit = int(bit, 2)
        result.append(bit)
    return bytearray(result)


def encode_number(number, width=8):
    return bin(number)[2:].zfill(width)
