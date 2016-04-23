from flask import request, render_template, make_response

from subtitools.processing.exceptions import InvalidSrtFormatError
from web.business import subtitles


def get():
    response = make_response(subtitles.get())
    response.headers["Content-Disposition"] = "attachment; filename=output.srt"
    return response


def post():
    file_srt = request.files['file']
    try:
        subtitles.post(file_srt)
    except InvalidSrtFormatError:
        return make_response(
            ("The uploaded file is not a valid srt file", 400, {}))
    else:
        return make_response(('', 200, {}))


def get_preview():
    return render_template('subtitles.html', subtitles=subtitles.get_preview())
