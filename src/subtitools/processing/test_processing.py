import os
import unittest
import processing


class ProcessingTestCase(unittest.TestCase):
    def setUp(self):
        self.project_path = os.path.sep.join([os.path.dirname(os.path.realpath(__file__)), '..', '..', '..'])
        self.file_srt_path = os.path.sep.join([self.project_path, 'data', 'sherlock_03x01.srt'])

    def tearDown(self):
        pass

    def test_output_is_different_to_input(self):
        with open(self.file_srt_path, 'r') as input:
            lines_input = []
            for line in input:
                lines_input.append(line)
            processor = processing.NaiveProcessor(25)
            lines_output = []
            for line in processor.process(lines_input):
                lines_output.append(line)
        self.assertEqual(len(lines_input), len(lines_output), "The number of lines must be the same")
        lines_different = []
        for i in range(len(lines_input)):
            if lines_input[i] != lines_output[i]:
                lines_different.append(lines_output[i])
        self.assertGreater(len(lines_different), 0, "The output must be different to the input")

if __name__ == '__main__':
    unittest.main()
