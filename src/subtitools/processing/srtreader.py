"""
Reads SubRip text files (.srt files) and transforms them into its equivalent data structure.
A SubRip text file consists of a sequence of N subtitles, each of which following the structure:

1. A number indicating which subtitle it is in the sequence.
2. The time that the subtitle should appear on the screen, and then disappear.
3. The subtitle itself.
4. A blank line indicating the start of a new subtitle.

Example:
1
00:00:04,340 --> 00:00:05,780
JOHN: Sherlock!

2
00:00:14,060 --> 00:00:15,899
Its a trick.

For further information see http://www.matroska.org/technical/specs/subtitles/srt.html.
"""

import re
import logging

from subtitle import Subtitle
from exceptions import InvalidSrtFormatError

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SrtReader(object):
    def __init__(self, srt_file_path):
        self.srt_file_path = srt_file_path
        self.srt_file = open(self.srt_file_path, 'r')
        self.re_timestamps = re.compile('^(\d\d[:]\d\d[:]\d\d,\d\d\d)[ ][-][-][>][ ](\d\d[:]\d\d[:]\d\d[,]\d\d\d)$')

    def read_identifier(self):
        line_identifier = self.srt_file.readline()
        if line_identifier == '':
            raise EOFError("Unexpected end of file")
        try:
            identifier = int(line_identifier)
        except ValueError:
            raise InvalidSrtFormatError(InvalidSrtFormatError.MSG_IDENTIFIER_MUST_BE_INTEGER)
        return identifier

    def read_timestamps(self):
        line_timestamps = self.srt_file.readline()
        match_timestamps = self.re_timestamps.search(line_timestamps)
        if match_timestamps is None:
            raise InvalidSrtFormatError(InvalidSrtFormatError.MSG_TIMESTAMPS_FORMAT)
        return match_timestamps.groups()

    def read_text(self):
        line_text = self.srt_file.readline()
        if line_text in ('\n', ''):
            raise InvalidSrtFormatError(InvalidSrtFormatError.MSG_TEXT_MUST_HAVE_ONE_LINE)
        text = line_text
        line_text = self.srt_file.readline()
        while line_text != '\n':
            if line_text == '':
                raise InvalidSrtFormatError(InvalidSrtFormatError.MSG_SUBTITLE_MUST_END_WITH_NEWLINE)
            text += line_text
            line_text = self.srt_file.readline()
        return text

    def read_next_subtitle(self):
        subtitle = Subtitle()
        subtitle.identifier = self.read_identifier()
        subtitle.timestamp_begin, subtitle.timestamp_end = self.read_timestamps()
        subtitle.text = self.read_text()
        return subtitle

    def read_next_subtitles(self):
        while True:
            try:
                yield self.read_next_subtitle()
            except EOFError:
                return

    def read_subtitles(self):
        self.srt_file.seek(0)
        return [subtitle for subtitle in self.read_next_subtitles()]
