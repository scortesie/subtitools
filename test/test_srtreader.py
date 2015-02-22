# coding=utf-8
import os
import logging
import unittest

from src.subtitools.processing.srtreader import SrtReader
from src.subtitools.processing.exceptions import InvalidSrtFormatError
from src.subtitools.processing.subtitle import Subtitle

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SrtReaderTestCase(unittest.TestCase):
    def setUp(self):
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.data_path = os.path.join(self.test_path, 'data')
        self.file_srt_2_subtitles_path = os.path.join(self.data_path, 'srt-2_subtitles.srt')
        self.file_srt_2_subtitles_utf8_path = os.path.join(self.data_path, 'srt-2_subtitles_utf8.srt')
        self.file_srt_invalid_identifier = os.path.join(self.data_path, 'srt-invalid_identifier.srt')
        self.file_srt_invalid_timestamps = os.path.join(self.data_path, 'srt-invalid_timestamps.srt')
        self.file_srt_invalid_text_has_no_lines = os.path.join(self.data_path, 'srt-invalid_text_has_no_lines.srt')
        self.file_srt_invalid_text_is_eof = os.path.join(self.data_path, 'srt-invalid_text_is_eof.srt')
        self.file_srt_invalid_subtitle_ends_without_newline = os.path.join(
            self.data_path, 'srt-invalid_subtitle_ends_without_newline.srt')

    def tearDown(self):
        pass

    def test_should_read_next_subtitle_containing_1_line_text_and_next_subtitle_containing_2_lines_text(self):
        reader = SrtReader(self.file_srt_2_subtitles_path)

        subtitle = reader.read_next_subtitle()
        self.assertEqual(subtitle.identifier, 1249)
        self.assertEqual(subtitle.timestamp_begin, '01:24:09,860')
        self.assertEqual(subtitle.timestamp_end, '01:24:11,300')
        self.assertEqual(subtitle.text, 'I heard you.\n')

        subtitle = reader.read_next_subtitle()
        self.assertEqual(subtitle.identifier, 1250)
        self.assertEqual(subtitle.timestamp_begin, '01:24:15,020')
        self.assertEqual(subtitle.timestamp_end, '01:24:17,900')
        self.assertEqual(subtitle.text, 'Anyway, time to go and\nbe Sherlock Holmes.\n')

    def test_should_raise_invalid_format_error_when_reading_next_subtitle_with_invalid_identifier(self):
        reader = SrtReader(self.file_srt_invalid_identifier)
        with self.assertRaises(InvalidSrtFormatError):
            reader.read_next_subtitle()

    def test_should_raise_invalid_format_error_when_reading_next_subtitle_with_invalid_timestamps(self):
        reader = SrtReader(self.file_srt_invalid_timestamps)
        with self.assertRaises(InvalidSrtFormatError):
            reader.read_next_subtitle()

    def test_should_raise_invalid_format_error_when_reading_next_subtitle_with_invalid_text_has_no_lines(self):
        reader = SrtReader(self.file_srt_invalid_text_has_no_lines)
        with self.assertRaises(InvalidSrtFormatError):
            reader.read_next_subtitle()

    def test_should_raise_invalid_format_error_when_reading_next_subtitle_with_invalid_text_is_eof(self):
        reader = SrtReader(self.file_srt_invalid_text_is_eof)
        with self.assertRaises(InvalidSrtFormatError):
            reader.read_next_subtitle()

    def test_should_raise_invalid_format_error_when_reading_next_subtitle_ends_without_newline(self):
        reader = SrtReader(self.file_srt_invalid_subtitle_ends_without_newline)
        with self.assertRaises(InvalidSrtFormatError):
            reader.read_next_subtitle()

    def test_should_read_subtitles(self):
        subtitle_1 = Subtitle(1249, '01:24:09,860', '01:24:11,300', 'I heard you.\n')
        subtitle_2 = Subtitle(1250, '01:24:15,020', '01:24:17,900', 'Anyway, time to go and\nbe Sherlock Holmes.\n')
        subtitles_reference = [subtitle_1, subtitle_2]
        reader = SrtReader(self.file_srt_2_subtitles_path)
        subtitles = reader.read_subtitles()
        self.assertEqual(subtitles_reference, subtitles)

    def test_should_read_subtitles_utf8(self):
        subtitle_1 = Subtitle(1249, '01:24:09,860', '01:24:11,300', 'Te escuché.\n')
        subtitle_2 = Subtitle(1250, '01:24:15,020', '01:24:17,900', '¡Qué más da, es hora de\nser Sherlock Holmes!\n')
        subtitles_reference = [subtitle_1, subtitle_2]
        reader = SrtReader(self.file_srt_2_subtitles_utf8_path)
        subtitles = reader.read_subtitles()
        self.assertEqual(subtitles_reference, subtitles)
