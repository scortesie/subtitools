import os

import flask

from controllers import subtitles

app = flask.Flask(__name__, static_url_path='/static')
app.secret_key = os.environ['APP_SECRET_KEY']


@app.route('/')
def index():
    return flask.render_template('index.html', subtitles=[])


@app.route('/subtitles', methods=('GET',), strict_slashes=False)
def subtitles_get():
    return subtitles.get()


@app.route('/subtitles', methods=('POST',), strict_slashes=False)
def subtitles_post():
    return subtitles.post()


@app.route('/preview', methods=('GET',), strict_slashes=False)
def preview_get():
    return subtitles.get_preview()


if __name__ == '__main__':
    app.run(debug=True)
