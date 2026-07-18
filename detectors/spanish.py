SPANISH = {

    0xC1: "Á",
    0xC9: "É",
    0xCD: "Í",
    0xD3: "Ó",
    0xDA: "Ú",
    0xD1: "Ñ",

    0xE1: "á",
    0xE9: "é",
    0xED: "í",
    0xF3: "ó",
    0xFA: "ú",
    0xF1: "ñ",
}

class Detector:

    def begin(self, result):

        result.statistics["spanish"] = {}

    def process(self, block, offset, result):

        pass

    def end(self, result):

        for b, c in SPANISH.items():

            result.statistics["spanish"][c] = result.byte_frequency[b]