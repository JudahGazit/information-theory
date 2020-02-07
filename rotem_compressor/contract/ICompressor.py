class ICompressor(object):
    def compress(self, data):
        raise NotImplementedError()

    def decompress(self, compressed):
        raise NotImplementedError()