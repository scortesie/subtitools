from src.subtitools.processing.subtitle import Subtitle


class Tuner(object):
    def __init__(self):
        self.filters = []

    def add_filter(self, filter_to_add):
        self.filters.append(filter_to_add)

    def tune(self, subtitles_input_file):
        subtitle_1 = Subtitle(1249, '01:24:09,860', '01:24:11,300', '_ heard you.\n')
        subtitle_2 = Subtitle(1250, '01:24:15,020', '01:24:17,900', '______, time to go ___\nbe Sherlock Holmes.\n')
        return [subtitle_1, subtitle_2]