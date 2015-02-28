import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SrtWriter(object):
    def __init__(self, srt_file_path):
        self.srt_file_path = srt_file_path
        self.srt_file = open(self.srt_file_path, 'w')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.srt_file.close()

    def write_subtitle(self, subtitle):
        self.srt_file.write(str(subtitle))

    def write_subtitles(self, subtitles):
        for subtitle in subtitles:
            self.write_subtitle(subtitle)

    def close(self):
        self.srt_file.close()
