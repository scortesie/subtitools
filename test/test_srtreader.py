import os
import unittest

from src.subtitools.processing.srtreader import SrtReader
from src.subtitools.processing.exceptions import InvalidSrtFormatError


class SrtReaderTestCase(unittest.TestCase):
    def setUp(self):
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.data_path = os.path.join(self.test_path, 'data')
        self.file_srt_2_subtitles_path = os.path.join(self.data_path, 'srt-2_subtitles.srt')
        self.file_srt_invalid_identifier = os.path.join(self.data_path, 'srt-invalid_identifier.srt')
        self.file_srt_invalid_timestamps = os.path.join(self.data_path, 'srt-invalid_timestamps.srt')

    def tearDown(self):
        pass

    def test_read_next(self):
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

    def test_read_next_invalid_identifier(self):
        reader = SrtReader(self.file_srt_invalid_identifier)
        with self.assertRaises(InvalidSrtFormatError):
            reader.read_next_subtitle()

    def test_read_next_invalid_timestamps(self):
        reader = SrtReader(self.file_srt_invalid_timestamps)
        with self.assertRaises(InvalidSrtFormatError):
            reader.read_next_subtitle()
