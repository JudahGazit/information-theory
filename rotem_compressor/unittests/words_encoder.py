from rotem_compressor.unittests.compression_testcase import CompressionTestCase
from rotem_compressor.words_encoder import WordsEncoder


class WordsEncoderTests(CompressionTestCase):
    compressor = WordsEncoder()