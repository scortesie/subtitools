Subtitools
==========

Subtitools is a set of tools for subtitle processing.

See a demo on Heroku, [https://subtitools.herokuapp.com/](https://subtitools.herokuapp.com/).

## Python API usage

The following code snippet shows how to read a srt file containing subtitles
and write them into a second file:

```
import sys

from subtitools.processing.srtreader import SrtReader
from subtitools.processing.srtwriter import SrtWriter
from subtitools.processing.exceptions import InvalidSrtFormatError

with SrtReader('tlo.srt') as reader, SrtWriter(sys.stdout) as writer:
    try:
        for subtitle in reader:
            writer.write(subtitle)
    except InvalidSrtFormatError as e:
        sys.stdout.write(
            "There was an error while reading the file: {0}".format(
                e.message))
```
