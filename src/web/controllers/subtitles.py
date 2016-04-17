from flask import request, render_template, make_response

from web.business import subtitles


def get():
    response = make_response(subtitles.get())
    response.headers["Content-Disposition"] = "attachment; filename=output.srt"
    return response


def post():
    file_srt = request.files['file']
    subtitles.post(file_srt)
    return make_response(('', 200, {}))


def get_preview():
    return render_template('subtitles.html', subtitles=subtitles.get_preview())
