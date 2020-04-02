def to_bytearray(values):
    byte_array = []
    if isinstance(values, bytearray):
        return values
    for item in values:
        if isinstance(item, str):
            for c in item:
                byte_array.extend(ord(c).to_bytes(2, 'big'))
        else:
            byte_array.extend(item.to_bytes(2, 'big'))
    return bytearray(byte_array)


def from_bytearray(values, as_string=True):
    result = []
    for index in range(0, len(values), 2):
        first, second = values[index:index + 2]
        first = first if isinstance(first, int) else ord(first)
        second = second if isinstance(second, int) else ord(second)
        value = int.from_bytes([first, second], 'big')
        value = chr(value) if as_string else value
        result.append(value)
    result = bytearray(map(ord, result))
    return result


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
