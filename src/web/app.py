import sys
import os

import flask
from flask import request, session

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')
from subtitools.processing.subtitle import Subtitle
from subtitools.processing.exceptions import InvalidSrtFormatError
from subtitools.processing.tuner import Tuner
from subtitools.processing.filter import HideTextFilter
from subtitools.processing.srtreader import SrtReader
from subtitools.processing.srtwriter import SrtWriter
from json_encoder import SubtitoolsJSONEncoder


app = flask.Flask(__name__, static_url_path='/static')
app.secret_key = 'this will be our secret'
app.json_encoder = SubtitoolsJSONEncoder


@app.route('/')
def index():
    return flask.render_template('index.html', subtitles=[])


@app.route('/upload/', methods=('POST',))
def upload():
    file_srt = request.files['file']
    with SrtReader(file_srt) as reader:
        subtitles = reader.read_subtitles()
        session['subtitles'] = subtitles[:10]
    return ''


@app.route('/subtitles/', methods=('GET',))
def preview_subtitles():
    subtitles = []
    if 'subtitles' in session:
        subtitles = [Subtitle.get_instance_from_json(subtitle)
                     for subtitle in session['subtitles']]
    return flask.render_template('subtitles.html', subtitles=subtitles)


if __name__ == '__main__':
    app.run(debug=True)
