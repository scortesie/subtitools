#!/usr/bin/python

# Hides a specific percentage of the words of a SubRip file (*.srt) replacing each of the characters by the underscore.
# Example: Hide 25% of the words of /home/santiago/Desktop/sherlock_01x02.srt:
# $ hide-subtitles.py -p 25 \
#                     /home/santiago/Desktop/sherlock_01x02.srt \
#                     /home/santiago/Desktop/sherlock_01x02-hidden-25.srt

import sys
import argparse
import random
import re


class Processor(object):
    def __init__(self, hide_percentage):
        self.hide_percentage = hide_percentage
        random.seed()


class NaiveProcessor(Processor):
    ID = 1
    TIME = 2
    TEXT = 3
    END = 4

    def __init__(self, hide_percentage):
        super(NaiveProcessor, self).__init__(hide_percentage)
    
    def hide_words_in_line(self, text):
        return ' '.join([re.sub('.', '_', word) if random.random() < self.hide_percentage * 0.01 and '<' not in word else word for word in text.split()]) + '\n'

    def process(self, input):
        state = self.ID
        for line in input:
            if len(line) == 0 or line.strip() == '':
                state = self.END
            if state == self.ID:
                yield line
                state = self.TIME
                continue
            elif state == self.TIME:
                yield line
                state = self.TEXT
                continue
            elif state == self.TEXT:
                processed_line = self.hide_words_in_line(line)
                yield processed_line
                continue
            elif state == self.END:
                yield line
                state = self.ID
                continue


def main():
    default_hide_percentage = 30
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input', type=str, nargs='?', default=sys.stdin, help='input file, default is standard input')
    arg_parser.add_argument('output', type=str, nargs='?', default=sys.stdout, help='output file, default is standard output')
    arg_parser.add_argument('-p', '--percentage', type=int, default=default_hide_percentage, help='percentage of hidden words, default is {0}'.format(default_hide_percentage))
    args = arg_parser.parse_args()

    input = args.input
    output = args.output
    hide_percentage = args.percentage

    if input != sys.stdin:
        try:
            input = open(input, "r")
        except IOError:
            sys.stderr.write("Error: File '{0}' does not exist\n".format(input))
            sys.exit(1)
    if output != sys.stdout:
        output = open(output, "w")
  
    processor = NaiveProcessor(hide_percentage)
    for line in processor.process(input):
        output.write(line)

    sys.exit(0)


if __name__ == "__main__":
    main()
