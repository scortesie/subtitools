import logging

from subtitools.processing.subtitle import Subtitle

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SrtWriter(object):
    def __init__(self, srt_file):
        if type(srt_file) is str:
            self.srt_file = open(srt_file, 'w')
        else:
            self.srt_file = srt_file

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _write_subtitle(self, subtitle):
        self.srt_file.write(str(subtitle))
        self.srt_file.write('\n')

    def _write_subtitles(self, subtitles):
        for subtitle in subtitles:
            self._write_subtitle(subtitle)

    def write(self, subtitles):
        if isinstance(subtitles, Subtitle):
            self._write_subtitle(subtitles)
        elif hasattr(subtitles, '__iter__'):
            self._write_subtitles(subtitles)
        else:
            raise ValueError(
                "The provided object has not a valid writable type")

    def close(self):
        self.srt_file.close()
