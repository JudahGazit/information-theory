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
    return result


def encode_number(number, width=8):
    return bin(number)[2:].zfill(width)

def pop_number(numbers, width=8):
    numbers_bin = ''.join([encode_number(number, 8) for number in numbers])
    popped = int(numbers_bin[:width], 2)
    rest = numbers_bin[width:]
    return popped, bits_to_numbers(rest)

def bits_to_numbers(bits):
    result = [int(bits[index:index + 8], 2) for index in range(0, len(bits), 8)]
    return bytearray(result)
