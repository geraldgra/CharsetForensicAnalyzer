from core.reader import read_blocks

class AnalyzerEngine:

    def __init__(self):
        self.detectors = []

    def add_detector(self, detector):
        self.detectors.append(detector)

    def analyze(self, path, result):

        #
        # Inicio
        #

        for detector in self.detectors:
            if hasattr(detector, "begin"):
                detector.begin(result)

        #
        # Lectura única del archivo
        #

        for block, offset in read_blocks(path):
            for detector in self.detectors:
                detector.process(block, offset, result)

        #
        # Final
        #

        for detector in self.detectors:
            if hasattr(detector, "end"):
                detector.end(result)