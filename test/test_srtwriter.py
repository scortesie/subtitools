# coding=utf-8
import os
import logging
import unittest
from subtitools.processing.srtreader import SrtReader
from subtitools.processing.srtwriter import SrtWriter
from subtitools.processing.subtitle import Subtitle

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SrtWriterTestCase(unittest.TestCase):
    def setUp(self):
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.data_path = os.path.join(self.test_path, 'data')
        self.file_srt_2_subtitles_path = os.path.join(self.data_path, 'srt-2_subtitles.srt')
        self.file_srt_2_subtitles_utf8_path = os.path.join(self.data_path, 'srt-2_subtitles_utf8.srt')
        self.file_srt_temp_path = os.path.join(self.data_path, 'srt-temp.srt')

    def tearDown(self):
        if os.path.isfile(self.file_srt_temp_path):
            os.remove(self.file_srt_temp_path)

    def test_should_write_1_subtitle(self):
        subtitle = Subtitle(1249, '01:24:09,860', '01:24:11,300', 'I heard you.\n')
        subtitle_serialised = '1249\n01:24:09,860 --> 01:24:11,300\nI heard you.\n\n'
        with SrtWriter(self.file_srt_temp_path) as writer:
            writer.write(subtitle)
        with open(self.file_srt_temp_path) as file_str_temp:
            self.assertEqual(subtitle_serialised, file_str_temp.read())

    def test_should_write_2_subtitles(self):
        subtitle_1 = Subtitle(1249, '01:24:09,860', '01:24:11,300', 'I heard you.\n')
        subtitle_1_serialised = '1249\n01:24:09,860 --> 01:24:11,300\nI heard you.\n\n'
        subtitle_2 = Subtitle(1250, '01:24:15,020', '01:24:17,900', 'Anyway, time to go and\nbe Sherlock Holmes.\n')
        subtitle_2_serialised = '1250\n01:24:15,020 --> 01:24:17,900\nAnyway, time to go and\nbe Sherlock Holmes.\n\n'
        with SrtWriter(self.file_srt_temp_path) as writer:
            writer.write(subtitle_1)
            writer.write(subtitle_2)
        with open(self.file_srt_temp_path) as file_str_temp:
            self.assertEqual(subtitle_1_serialised + subtitle_2_serialised, file_str_temp.read())

    def test_should_write_all_subtitles(self):
        subtitle_1 = Subtitle(1249, '01:24:09,860', '01:24:11,300', 'I heard you.\n')
        subtitle_1_serialised = '1249\n01:24:09,860 --> 01:24:11,300\nI heard you.\n\n'
        subtitle_2 = Subtitle(1250, '01:24:15,020', '01:24:17,900', 'Anyway, time to go and\nbe Sherlock Holmes.\n')
        subtitle_2_serialised = '1250\n01:24:15,020 --> 01:24:17,900\nAnyway, time to go and\nbe Sherlock Holmes.\n\n'
        subtitles = [subtitle_1, subtitle_2]
        with SrtWriter(self.file_srt_temp_path) as writer:
            writer.write(subtitles)
        with open(self.file_srt_temp_path) as file_str_temp:
            self.assertEqual(subtitle_1_serialised + subtitle_2_serialised, file_str_temp.read())

    def test_should_write_all_subtitles_utf8(self):
        subtitle_1 = Subtitle(1249, '01:24:09,860', '01:24:11,300', 'Te escuché.\n')
        subtitle_1_serialised = '1249\n01:24:09,860 --> 01:24:11,300\nTe escuché.\n\n'
        subtitle_2 = Subtitle(1250, '01:24:15,020', '01:24:17,900', '¡Qué más da, es hora de\nser Sherlock Holmes!\n')
        subtitle_2_serialised = '1250\n01:24:15,020 --> 01:24:17,900\n¡Qué más da, es hora de\nser Sherlock Holmes!\n\n'
        subtitles = [subtitle_1, subtitle_2]
        with SrtWriter(self.file_srt_temp_path) as writer:
            writer.write(subtitles)
        with open(self.file_srt_temp_path) as file_str_temp:
            self.assertEqual(subtitle_1_serialised + subtitle_2_serialised, file_str_temp.read())

    def test_should_read_and_write_all_subtitles(self):
        reader = SrtReader(self.file_srt_2_subtitles_path)
        subtitles = reader.read_subtitles()
        with SrtWriter(self.file_srt_temp_path) as writer:
            writer.write(subtitles)
        with open(self.file_srt_2_subtitles_path) as file_srt_2_subtitles,\
                open(self.file_srt_temp_path) as file_srt_temp:
            self.assertEqual(file_srt_2_subtitles.read(), file_srt_temp.read())

    def test_should_read_and_write_all_subtitles_utf8(self):
        reader = SrtReader(self.file_srt_2_subtitles_utf8_path)
        subtitles = reader.read_subtitles()
        with SrtWriter(self.file_srt_temp_path) as writer:
            writer.write(subtitles)
        with open(self.file_srt_2_subtitles_utf8_path) as file_srt_2_subtitles_utf8,\
                open(self.file_srt_temp_path) as file_srt_temp:
            self.assertEqual(file_srt_2_subtitles_utf8.read(), file_srt_temp.read())
