class Detector:

    def begin(self, result):

        result.utf8_valid = True
        result.utf8_errors = 0

        result.statistics["ascii"] = 0
        result.statistics["utf8_2"] = 0
        result.statistics["utf8_3"] = 0
        result.statistics["utf8_4"] = 0
        result.statistics["invalid_utf8"] = 0

        self.pending = b""

    def process(self, block, offset, result):

        #
        # Unir bytes pendientes
        #

        if self.pending:

            block = self.pending + block

            offset -= len(self.pending)

            self.pending = b""

        i = 0

        while i < len(block):

            b = block[i]

            result.total_bytes_analyzed += 1

            #
            # ASCII
            #

            if b <= 0x7F:

                result.statistics["ascii"] += 1

                i += 1

                continue

            #
            # UTF8 2 bytes
            #

            if (b & 0xE0) == 0xC0:

                need = 2

            #
            # UTF8 3 bytes
            #

            elif (b & 0xF0) == 0xE0:

                need = 3

            #
            # UTF8 4 bytes
            #

            elif (b & 0xF8) == 0xF0:

                need = 4

            else:

                self.error(result, offset + i)

                i += 1

                continue

            #
            # ¿La secuencia quedó cortada?
            #

            if i + need > len(block):

                self.pending = block[i:]

                break

            valid = True

            for j in range(1, need):

                if (block[i + j] & 0xC0) != 0x80:

                    valid = False

                    break

            if not valid:

                self.error(result, offset + i)

                i += 1

                continue

            if need == 2:

                result.statistics["utf8_2"] += 1

            elif need == 3:

                result.statistics["utf8_3"] += 1

            else:

                result.statistics["utf8_4"] += 1

            i += need

    def end(self, result):

        #
        # Si quedaron bytes pendientes
        #

        if self.pending:

            self.error(result, result.total_bytes_analyzed)

    def error(self, result, offset):

        result.utf8_valid = False

        result.utf8_errors += 1

        result.statistics["invalid_utf8"] += 1

        if result.first_utf8_error_offset is None:

            result.first_utf8_error_offset = offset

        result.last_utf8_error_offset = offset