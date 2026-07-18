#
# Bytes imprimibles exclusivos de Windows-1252
#

WINDOWS1252_BYTES = {

    0x80,  # €
    0x82,  # ‚
    0x83,  # ƒ
    0x84,  # „
    0x85,  # …
    0x86,  # †
    0x87,  # ‡
    0x88,  # ˆ
    0x89,  # ‰
    0x8A,  # Š
    0x8B,  # ‹
    0x8C,  # Œ
    0x8E,  # Ž

    0x91,
    0x92,
    0x93,
    0x94,
    0x95,
    0x96,
    0x97,
    0x98,
    0x99,
    0x9A,
    0x9B,
    0x9C,
    0x9E,
    0x9F
}

#
# No están definidos en Windows-1252
#

UNDEFINED = {

    0x81,
    0x8D,
    0x8F,
    0x90,
    0x9D
}


class Detector:

    def begin(self, result):

        result.windows1252_bytes = 0
        result.iso_control_bytes = 0
        result.undefined_details = {}

    def process(self, block, offset, result):

        for i, b in enumerate(block):

            if b not in UNDEFINED:
                continue

            result.iso_control_bytes += 1

            if b not in result.undefined_details:

                start = max(0, i - 8)
                end = min(len(block), i + 9)
                context = block[start:end]

                result.undefined_details[b] = {
                    "count": 1,
                    "offset": offset + i,
                    "context": context
                }

            else:
                result.undefined_details[b]["count"] += 1

    def end(self, result):

        for b in WINDOWS1252_BYTES:

            result.windows1252_bytes += result.byte_frequency[b]

        #
        # Primera heurística
        #

        if result.utf8_valid:
            result.likely_encoding = "UTF-8"
            result.confidence = 99.0
            return

        if result.windows1252_bytes > 0:
            result.likely_encoding = "Windows-1252"
            result.confidence = 95.0
            return

        result.likely_encoding = "ISO-8859-1 (posible)"
        result.confidence = 70.0