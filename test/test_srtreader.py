# -*- coding: utf-8 -*-

import os
import logging
import unittest

from subtitools.processing.srtreader import SrtReader
from subtitools.processing.exceptions import InvalidSrtFormatError
from subtitools.processing.subtitle import Subtitle

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
        self.file_srt_invalid_more_than_1_newlines_after_subtitle = os.path.join(
            self.data_path, 'srt-invalid_more_than_1_newlines_after_subtitle.srt')
        self.file_srt_actual_non_strict = os.path.join(self.data_path, 'srt-actual_non_strict.srt')
        self.file_srt_with_bom = os.path.join(self.data_path, 'srt-with_bom.srt')

    def tearDown(self):
        pass

    def test_should_read_next_subtitle_containing_1_line_text_and_next_subtitle_containing_2_lines_text(self):
        with SrtReader(self.file_srt_2_subtitles_path) as reader:
            subtitle = reader.read_next_subtitle()
            self.assertEqual(subtitle.identifier, 1249)
            self.assertEqual(subtitle.timestamp_begin, '01:24:09,860')
            self.assertEqual(subtitle.timestamp_end, '01:24:11,300')
            self.assertEqual(subtitle.text, u'I heard you.\n')
            subtitle = reader.read_next_subtitle()
            self.assertEqual(subtitle.identifier, 1250)
            self.assertEqual(subtitle.timestamp_begin, '01:24:15,020')
            self.assertEqual(subtitle.timestamp_end, '01:24:17,900')
            self.assertEqual(subtitle.text, u'Anyway, time to go and\nbe Sherlock Holmes.\n')

    def test_should_raise_invalid_format_error_when_reading_next_subtitle_with_invalid_identifier(self):
        reader = SrtReader(self.file_srt_invalid_identifier)
        with self.assertRaises(InvalidSrtFormatError):
            reader.read_next_subtitle()

    def test_should_raise_invalid_format_error_when_reading_next_subtitle_with_invalid_timestamps(self):
        reader = SrtReader(self.file_srt_invalid_timestamps)
        with self.assertRaises(InvalidSrtFormatError):
            reader.read_next_subtitle()

    def test_should_raise_invalid_format_error_when_next_subtitle_text_has_no_lines_in_strict_parsing(self):
        reader = SrtReader(self.file_srt_invalid_text_has_no_lines, True)
        with self.assertRaises(InvalidSrtFormatError):
            reader.read_next_subtitle()

    def test_should_read_next_subtitle_when_text_has_no_lines_in_non_strict_parsing(self):
        with SrtReader(self.file_srt_invalid_text_has_no_lines, False) as reader:
            subtitle = reader.read_next_subtitle()
            self.assertEqual(subtitle.identifier, 1249)
            self.assertEqual(subtitle.timestamp_begin, '01:24:09,860')
            self.assertEqual(subtitle.timestamp_end, '01:24:11,300')
            self.assertEqual(subtitle.text, '\n')
            subtitle = reader.read_next_subtitle()
            self.assertEqual(subtitle.identifier, 1250)
            self.assertEqual(subtitle.timestamp_begin, '01:24:15,020')
            self.assertEqual(subtitle.timestamp_end, '01:24:17,900')
            self.assertEqual(subtitle.text, u'Anyway, time to go and\nbe Sherlock Holmes.\n')

    def test_should_raise_invalid_format_error_when_reading_next_subtitle_with_invalid_text_is_eof(self):
        reader = SrtReader(self.file_srt_invalid_text_is_eof)
        with self.assertRaises(InvalidSrtFormatError):
            reader.read_next_subtitle()

    def test_should_raise_invalid_format_error_when_reading_next_subtitle_ends_without_newline(self):
        reader = SrtReader(self.file_srt_invalid_subtitle_ends_without_newline)
        with self.assertRaises(InvalidSrtFormatError):
            reader.read_next_subtitle()

    def test_should_read_subtitles(self):
        subtitle_1 = Subtitle(1249, '01:24:09,860', '01:24:11,300', u'I heard you.\n')
        subtitle_2 = Subtitle(1250, '01:24:15,020', '01:24:17,900', u'Anyway, time to go and\nbe Sherlock Holmes.\n')
        subtitles_reference = [subtitle_1, subtitle_2]
        with SrtReader(self.file_srt_2_subtitles_path) as reader:
            subtitles = reader.read_subtitles()
            self.assertEqual(subtitles_reference, subtitles)

    def test_should_read_subtitles_utf8(self):
        subtitle_1 = Subtitle(1249, '01:24:09,860', '01:24:11,300', u'Te escuché.\n')
        subtitle_2 = Subtitle(1250, '01:24:15,020', '01:24:17,900', u'¡Qué más da, es hora de\nser Sherlock Holmes!\n')
        subtitles_reference = [subtitle_1, subtitle_2]
        with SrtReader(self.file_srt_2_subtitles_utf8_path) as reader:
            subtitles = reader.read_subtitles()
            self.assertEqual(subtitles_reference, subtitles)

    def test_should_read_next_subtitle_when_more_than_1_newlines_after_subtitle(self):
        with SrtReader(self.file_srt_invalid_more_than_1_newlines_after_subtitle, False) as reader:
            subtitle = reader.read_next_subtitle()
            self.assertEqual(subtitle.identifier, 758)
            self.assertEqual(subtitle.timestamp_begin, '00:55:36,000')
            self.assertEqual(subtitle.timestamp_end, '00:55:39,440')
            self.assertEqual(subtitle.text, u'Chinese ceramic statue sold for\n')
            subtitle = reader.read_next_subtitle()
            self.assertEqual(subtitle.identifier, 759)
            self.assertEqual(subtitle.timestamp_begin, '00:55:39,440')
            self.assertEqual(subtitle.timestamp_end, '00:55:42,840')
            self.assertEqual(subtitle.text, u'Look, a month before that,\nChinese painting,\n')

    def test_should_read_actual_non_strict_srt_file(self):
        with SrtReader(self.file_srt_actual_non_strict, False) as reader:
            subtitles = [subtitle for subtitle in reader]
            self.assertEqual(1162, len(subtitles))

    def test_should_reset_srt_file(self):
        subtitle_1 = Subtitle(
            1,
            '00:00:07,130', '00:00:09,131',
            u'Uh, yeah, no.\n')
        subtitle_2 = Subtitle(
            2,
            '00:00:09,132', '00:00:11,133',
            u'I mean, you people called me.\n')
        with SrtReader(self.file_srt_with_bom, False) as reader:
            subtitle = reader.read_next_subtitle()
            self.assertEqual(subtitle, subtitle_1)
            subtitle = reader.read_next_subtitle()
            self.assertEqual(subtitle, subtitle_2)
            reader.reset()
            subtitle = reader.read_next_subtitle()
            self.assertEqual(subtitle, subtitle_1)
            subtitle = reader.read_next_subtitle()
            self.assertEqual(subtitle, subtitle_2)
