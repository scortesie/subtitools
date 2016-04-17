import StringIO

from subtitools.processing.srtreader import SrtReader
from subtitools.processing.srtwriter import SrtWriter
from web.helpers import session


def post(file_str):
    with SrtReader(file_str) as reader:
        subtitles = reader.read_subtitles_dict()
    session.set_subtitles(subtitles)
    session.set_preview(subtitles)


def get():
    subtitles_tuned = session.get_tuner().tune(session.get_subtitles())
    subtitles_file = StringIO.StringIO()
    with SrtWriter(subtitles_file) as writer:
        writer.write(subtitles_tuned)
        return subtitles_file.getvalue()


def get_preview():
    return session.get_preview()
