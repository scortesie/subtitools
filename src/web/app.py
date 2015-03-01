from StringIO import StringIO

import flask

from src.subtitools.processing.tuner import Tuner
from src.subtitools.processing.srtwriter import SrtWriter


app = flask.Flask(__name__, static_folder='./static/')


@app.route('/')
@app.route('/<path:filename>')
def serve_static(filename='index.html'):
    return app.send_static_file(filename)


@app.route('/tune_subtitles/', methods=['POST'])
def tune_subtitles():
    file_srt_to_tune = flask.request.files['file']

    tuner = Tuner()
    subtitles_tuned = tuner.tune(file_srt_to_tune)

    file_srt_tuned = StringIO()
    writer = SrtWriter(file_srt_tuned)
    writer.write_subtitles(subtitles_tuned)
    file_srt_tuned.seek(0)

    return flask.send_file(file_srt_tuned, mimetype='text/plain',
                           attachment_filename=file_srt_to_tune.filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
