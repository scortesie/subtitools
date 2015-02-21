import os
import unittest

from src.subtitools.processing.filter import HideTextFilter
from src.subtitools.processing.tuner import Tuner
from src.subtitools.processing.srtreader import SrtReader


class TunerTestCase(unittest.TestCase):
    def setUp(self):
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.data_path = os.path.join(self.test_path, 'data')
        self.file_srt_2_subtitles_path = os.path.join(self.data_path, 'srt-2_subtitles.srt')
        self.file_srt_2_subtitles_hide_25_path = os.path.join(self.data_path, 'srt-2_subtitles_hide_25.srt')

    def tearDown(self):
        pass

    def test_should_hide_25_percent_of_text(self):
        tuner = Tuner()
        tuner.add_filter(HideTextFilter(25))
        with open(self.file_srt_2_subtitles_path, 'r') as file_srt_2_subtitles:
            subtitles_tuned = tuner.tune(file_srt_2_subtitles)
        srt_reader = SrtReader(self.file_srt_2_subtitles_hide_25_path)
        subtitles_tuned_reference = srt_reader.read_file()
        self.assertEqual(subtitles_tuned_reference, subtitles_tuned)
