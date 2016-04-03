import sys
import os
from StringIO import StringIO

import flask
from flask import request

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')
from subtitools.processing.exceptions import InvalidSrtFormatError
from subtitools.processing.tuner import Tuner
from subtitools.processing.filter import HideTextFilter
from subtitools.processing.srtwriter import SrtWriter


app = flask.Flask(__name__, static_url_path='/static')
app.secret_key = 'this will be our secret'


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/tune_subtitles/', methods=['POST'])
def tune_subtitles():
    file_srt_to_tune = request.files['file']
    hide_text = True if request.form.get('hide_text') == 'true' else False

    tuner = Tuner()
    if hide_text:
        tuner.add_filter(HideTextFilter(25))

    try:
        subtitles_tuned = tuner.tune(file_srt_to_tune)
        file_srt_tuned = StringIO()
        writer = SrtWriter(file_srt_tuned)
        writer.write(subtitles_tuned)
        file_srt_tuned.seek(0)
        response = flask.send_file(
            file_srt_tuned,
            mimetype='text/plain',
            attachment_filename=file_srt_to_tune.filename,
            as_attachment=True)
    except InvalidSrtFormatError:
        flask.flash("The file is not a valid srt file")
        response = flask.render_template('index.html')
    return response

if __name__ == '__main__':
    app.run(debug=True)
