PATTERNS = [
    b"\xC3\x83",   # Ã
    b"\xC2\xA0",   # Â
    b"\xE2\x80",   # comillas, guiones...
]


class Detector:

    def begin(self, result):
        result.mojibake_patterns = {}
        result.mojibake_count = 0

    def process(self, block, offset, result):

        for pattern in PATTERNS:

            count = block.count(pattern)

            if count:

                result.mojibake_patterns[pattern.hex(" ")] = (
                    result.mojibake_patterns.get(pattern.hex(" "), 0)
                    + count
                )

                result.mojibake_count += count

    def end(self, result):
        pass