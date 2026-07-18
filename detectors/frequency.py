class Detector:

    def begin(self, result):
        pass

    def process(self, block, offset, result):

        for b in block:
            result.byte_frequency[b] += 1
        
        #
        # Byte NULL
        #
        if b == 0x00:
            result.null_bytes += 1

        #
        # Controles ASCII
        #
        elif b < 32 and b not in (9, 10, 13):
            result.control_bytes += 1

    def end(self, result):
        pass