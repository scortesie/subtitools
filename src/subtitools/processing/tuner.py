from subtitools.processing.srtreader import SrtReader


class Tuner(object):
    def __init__(self):
        self.filters = []

    def add_filter(self, tuning_filter):
        self.filters.append(tuning_filter)

    def tune(self, subtitles_file_path):
        subtitles_tuned = []
        srt_reader = SrtReader(subtitles_file_path)
        for subtitle in srt_reader.read_subtitles():
            subtitle_tuned = subtitle
            for tuning_filter in self.filters:
                subtitle_tuned = tuning_filter.filter(subtitle_tuned)
            subtitles_tuned.append(subtitle_tuned)
        return subtitles_tuned
