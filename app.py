import getopt
import sys

from rotem_compressor.rotem_compressor import RotemCompressor


def print_help(exit_code):
    print('test.py -i <input_file> -o <output_file>')
    sys.exit(exit_code)


def get_opts(argv):
    try:
        opts, args = getopt.getopt(argv, "hdi:o:")
    except getopt.GetoptError:
        print_help(2)
    if '-h' in opts:
        print_help(0)
    opts = dict(opts)
    input_file, output_file = opts.get('-i'), opts.get('-o')
    to_decompress = '-d' in opts
    return input_file, output_file, to_decompress


def compression(compressor, decompress, input_data, input_file, output_file):
    if decompress:
        print(f'decompressing file {input_file} to {output_file}')
        output_data = compressor.decompress(input_data)
    else:
        print(f'compressing file {input_file} to {output_file}')
        output_data = compressor.compress(input_data)
    return output_data


def main(argv):
    input_file, output_file, to_decompress = get_opts(argv)
    compressor = RotemCompressor()
    with open(input_file, 'rb') as f:
        input_data = f.read()
    output_data = compression(compressor, to_decompress, input_data, input_file, output_file)
    with open(output_file, 'wb') as f:
        f.write(output_data)


if __name__ == '__main__':
    main(sys.argv[1:])
