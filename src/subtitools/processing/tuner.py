

class Tuner(object):
    def __init__(self):
        self.filters = []

    def add_filter(self, tuning_filter):
        self.filters.append(tuning_filter)

    def tune(self, subtitle_iter):
        subtitles_tuned = []
        for subtitle in subtitle_iter:
            subtitle_tuned = subtitle
            for tuning_filter in self.filters:
                subtitle_tuned = tuning_filter.filter(subtitle_tuned)
            subtitles_tuned.append(subtitle_tuned)
        return subtitles_tuned
