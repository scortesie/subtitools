class Tuner(object):
    def __init__(self):
        self.filters = []

    def add_filter(self, filter_to_add):
        self.filters.append(filter_to_add)

    def tune(self, subtitles_input_file, subtitles_output_file):
        pass
