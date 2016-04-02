import sys
import os
import argparse

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')
from subtitools.processing.srtreader import SrtReader
from subtitools.processing.srtwriter import SrtWriter
from subtitools.processing.exceptions import InvalidSrtFormatError


def main():
    parser = argparse.ArgumentParser(description='Process subtitles.')
    parser.add_argument('srt_file',
                        help='path of the srt file containing the subtitles',
                        type=str,
                        nargs='?',
                        default=sys.stdin)
    parser.add_argument('output',
                        help='path of the output file',
                        type=str,
                        nargs='?',
                        default=sys.stdout)

    args = parser.parse_args()

    with SrtReader(args.srt_file) as reader, SrtWriter(args.output) as writer:
        try:
            for subtitle in reader:
                writer.write_subtitle(subtitle)
        except InvalidSrtFormatError as e:
            sys.stdout.write(
                "There was an error while reading the file: {0}".format(
                    e.message))
    return 0

if __name__ == '__main__':
    sys.exit(main())
