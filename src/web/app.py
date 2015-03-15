from StringIO import StringIO

import flask

from src.subtitools.processing.exceptions import InvalidSrtFormatError
from src.subtitools.processing.tuner import Tuner
from src.subtitools.processing.filter import HideTextFilter
from src.subtitools.processing.srtwriter import SrtWriter

app = flask.Flask(__name__, static_url_path='/static')
app.secret_key = 'this will be our secret'


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/tune_subtitles/', methods=['POST'])
def tune_subtitles():
    file_srt_to_tune = flask.request.files['file']
    hide_text = True if flask.request.form.get('hide_text') == 'true' else False

    tuner = Tuner()
    if hide_text:
        tuner.add_filter(HideTextFilter(25))

    try:
        subtitles_tuned = tuner.tune(file_srt_to_tune)
        file_srt_tuned = StringIO()
        writer = SrtWriter(file_srt_tuned)
        writer.write_subtitles(subtitles_tuned)
        file_srt_tuned.seek(0)
        response = flask.send_file(file_srt_tuned, mimetype='text/plain',
                                   attachment_filename=file_srt_to_tune.filename, as_attachment=True)
    except InvalidSrtFormatError:
        flask.flash("The file is not a valid srt file")
        response = flask.render_template('index.html')
    return response

if __name__ == '__main__':
    app.run(debug=True)
