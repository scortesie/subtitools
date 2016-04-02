import os
import logging
import unittest

from subtitools.processing.filter import HideTextFilter
from subtitools.processing.tuner import Tuner
from subtitools.processing.srtreader import SrtReader

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class TunerTestCase(unittest.TestCase):
    def setUp(self):
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.data_path = os.path.join(self.test_path, 'data')
        self.file_srt_2_subtitles_path = os.path.join(self.data_path, 'srt-2_subtitles.srt')
        self.file_srt_2_subtitles_hide_25_path = os.path.join(self.data_path, 'srt-2_subtitles_hide_25.srt')
        self.file_srt_2_subtitles_hide_50_path = os.path.join(self.data_path, 'srt-2_subtitles_hide_50.srt')
        self.file_srt_2_subtitles_hide_100_path = os.path.join(self.data_path, 'srt-2_subtitles_hide_100.srt')
        self.file_srt_2_subtitles_utf8_path = os.path.join(self.data_path, 'srt-2_subtitles_utf8.srt')
        self.file_srt_2_subtitles_utf8_hide_25_path = os.path.join(self.data_path, 'srt-2_subtitles_utf8_hide_25.srt')
        self.file_srt_2_subtitles_utf8_hide_50_path = os.path.join(self.data_path, 'srt-2_subtitles_utf8_hide_50.srt')
        self.file_srt_2_subtitles_utf8_hide_100_path = os.path.join(self.data_path, 'srt-2_subtitles_utf8_hide_100.srt')

    def tearDown(self):
        pass

    def test_should_not_tune_when_tuning_without_filters(self):
        srt_reader = SrtReader(self.file_srt_2_subtitles_path)
        subtitles = srt_reader.read_subtitles()
        tuner = Tuner()
        subtitles_tuned = tuner.tune(self.file_srt_2_subtitles_path)
        self.assertEqual(subtitles, subtitles_tuned)

    def test_should_hide_25_percent_of_text(self):
        tuner = Tuner()
        tuner.add_filter(HideTextFilter(25))
        subtitles_tuned = tuner.tune(self.file_srt_2_subtitles_path)
        srt_reader = SrtReader(self.file_srt_2_subtitles_hide_25_path)
        subtitles_tuned_reference = srt_reader.read_subtitles()
        self.assertEqual(subtitles_tuned_reference, subtitles_tuned)

    def test_should_hide_50_percent_of_text(self):
        tuner = Tuner()
        tuner.add_filter(HideTextFilter(50))
        subtitles_tuned = tuner.tune(self.file_srt_2_subtitles_path)
        srt_reader = SrtReader(self.file_srt_2_subtitles_hide_50_path)
        subtitles_tuned_reference = srt_reader.read_subtitles()
        self.assertEqual(subtitles_tuned_reference, subtitles_tuned)

    def test_should_hide_100_percent_of_text(self):
        tuner = Tuner()
        tuner.add_filter(HideTextFilter(100))
        subtitles_tuned = tuner.tune(self.file_srt_2_subtitles_path)
        srt_reader = SrtReader(self.file_srt_2_subtitles_hide_100_path)
        subtitles_tuned_reference = srt_reader.read_subtitles()
        self.assertEqual(subtitles_tuned_reference, subtitles_tuned)

    def test_should_hide_25_percent_of_text_utf8(self):
        tuner = Tuner()
        tuner.add_filter(HideTextFilter(25))
        subtitles_tuned = tuner.tune(self.file_srt_2_subtitles_utf8_path)
        srt_reader = SrtReader(self.file_srt_2_subtitles_utf8_hide_25_path)
        subtitles_tuned_reference = srt_reader.read_subtitles()
        self.assertEqual(subtitles_tuned_reference, subtitles_tuned)

    def test_should_hide_50_percent_of_text_utf8(self):
        tuner = Tuner()
        tuner.add_filter(HideTextFilter(50))
        subtitles_tuned = tuner.tune(self.file_srt_2_subtitles_utf8_path)
        srt_reader = SrtReader(self.file_srt_2_subtitles_utf8_hide_50_path)
        subtitles_tuned_reference = srt_reader.read_subtitles()
        self.assertEqual(subtitles_tuned_reference, subtitles_tuned)

    def test_should_hide_100_percent_of_text_utf8(self):
        tuner = Tuner()
        tuner.add_filter(HideTextFilter(100))
        subtitles_tuned = tuner.tune(self.file_srt_2_subtitles_utf8_path)
        srt_reader = SrtReader(self.file_srt_2_subtitles_utf8_hide_100_path)
        subtitles_tuned_reference = srt_reader.read_subtitles()
        self.assertEqual(subtitles_tuned_reference, subtitles_tuned)

    def test_should_raise_value_error_when_hiding_101_percent_of_text(self):
        tuner = Tuner()
        with self.assertRaises(ValueError):
            tuner.add_filter(HideTextFilter(101))

    def test_should_raise_value_error_when_hiding_0_percent_of_text(self):
        tuner = Tuner()
        with self.assertRaises(ValueError):
            tuner.add_filter(HideTextFilter(0))
