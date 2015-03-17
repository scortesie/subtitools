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
    def __init__(self, srt_file, apply_strict_parsing=False):
        if type(srt_file) is str:
            self.srt_file = open(srt_file, 'r')
        else:
            self.srt_file = srt_file
        self.apply_strict_parsing = apply_strict_parsing
        self.re_timestamps = re.compile('^(\d\d[:]\d\d[:]\d\d,\d\d\d)[ ][-][-][>][ ](\d\d[:]\d\d[:]\d\d[,]\d\d\d)$')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def read_identifier(self):
        line_identifier = self.srt_file.readline()
        if line_identifier == '':
            raise EOFError("Unexpected end of file")
        try:
            identifier = int(line_identifier)
        except ValueError:
            if self.apply_strict_parsing:
                raise InvalidSrtFormatError(InvalidSrtFormatError.MSG_IDENTIFIER_MUST_BE_INTEGER)
            else:
                if line_identifier in ('\n', '\r', '\r\n'):
                    identifier = self.read_identifier()
                else:
                    raise InvalidSrtFormatError(InvalidSrtFormatError.MSG_IDENTIFIER_MUST_BE_INTEGER)
        return identifier

    def read_timestamps(self):
        line_timestamps = self.srt_file.readline().rstrip()
        match_timestamps = self.re_timestamps.search(line_timestamps)
        if match_timestamps is None:
            logger.debug("line_timestamps: " + line_timestamps)
            raise InvalidSrtFormatError(InvalidSrtFormatError.MSG_TIMESTAMPS_FORMAT)
        return match_timestamps.groups()

    def read_text(self):
        line_text = self.srt_file.readline()
        if line_text == '':
            raise InvalidSrtFormatError(InvalidSrtFormatError.MSG_TEXT_MUST_HAVE_ONE_LINE)
        elif line_text in ('\n', '\r', '\r\n'):
            if self.apply_strict_parsing:
                raise InvalidSrtFormatError(InvalidSrtFormatError.MSG_TEXT_MUST_HAVE_ONE_LINE)
            else:
                logger.warning("The subtitle text is empty")
                return line_text
        text = line_text.rstrip() + '\n'
        line_text = self.srt_file.readline()
        while line_text not in ('\n', '\r', '\r\n'):
            if line_text == '':
                raise InvalidSrtFormatError(InvalidSrtFormatError.MSG_SUBTITLE_MUST_END_WITH_NEWLINE)
            text += line_text.rstrip() + '\n'
            line_text = self.srt_file.readline()
        return text

    def read_next_subtitle(self):
        subtitle = Subtitle()
        subtitle.identifier = self.read_identifier()
        subtitle.timestamp_begin, subtitle.timestamp_end = self.read_timestamps()
        subtitle.text = self.read_text()
        return subtitle

    def __iter__(self):
        return self

    def next(self):
        try:
            return self.read_next_subtitle()
        except EOFError:
            raise StopIteration()

    def read_next_subtitles(self):
        while True:
            try:
                yield self.read_next_subtitle()
            except EOFError:
                return

    def read_subtitles(self):
        self.srt_file.seek(0)
        return [subtitle for subtitle in self]

    def close(self):
        self.srt_file.close()
