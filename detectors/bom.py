UTF8_BOM = b'\xef\xbb\xbf'

UTF16_LE = b'\xff\xfe'

UTF16_BE = b'\xfe\xff'

UTF32_LE = b'\xff\xfe\x00\x00'

UTF32_BE = b'\x00\x00\xfe\xff'


class Detector:

    def begin(self, result):

        pass

    def process(self, block, offset, result):

        #
        # Solo mirar el primer bloque
        #

        if offset != 0:
            return

        if block.startswith(UTF8_BOM):

            result.bom = "UTF-8 BOM"

        elif block.startswith(UTF32_LE):

            result.bom = "UTF-32 LE"

        elif block.startswith(UTF32_BE):

            result.bom = "UTF-32 BE"

        elif block.startswith(UTF16_LE):

            result.bom = "UTF-16 LE"

        elif block.startswith(UTF16_BE):

            result.bom = "UTF-16 BE"

        else:

            result.bom = "No BOM"

    def end(self, result):

        pass