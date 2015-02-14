import os
import unittest

from src.subtitools.processing.filter import HideTextFilter
from src.subtitools.processing.tuner import Tuner


class TunerTestCase(unittest.TestCase):
    def setUp(self):
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.data_path = os.path.join(self.test_path, 'data')
        self.file_srt_sherlock_path = os.path.join(self.data_path, 'srt-sherlock_03x01.srt')
        self.file_output_1_path = os.path.join(self.data_path, 'output_1.srt')

    def tearDown(self):
        if os.path.isfile(self.file_output_1_path):
            os.remove(self.file_output_1_path)

    def test_tune_with_hide_text_filter(self):
        tuner = Tuner()
        tuner.add_filter(HideTextFilter(25))
        with open(self.file_srt_sherlock_path, 'r') as file_srt_sherlock,\
                open(self.file_output_1_path, 'w') as file_output_1:
            tuner.tune(file_srt_sherlock, file_output_1)
        self.assertTrue(os.path.isfile(self.file_output_1_path))
