import os

from flask import session

from subtitools.processing.subtitle import Subtitle
from subtitools.processing.tuner import Tuner
from subtitools.processing.filter import HideTextFilter
from web.data_access import subtitles as dao_subtitles

REMOVE_OLDER_THAN_MINUTES = int(
    os.environ.get('REMOVE_OLDER_THAN_MINUTES', 120))
SUBTITLES_PREVIEW_COUNT = int(os.environ.get('SUBTITLES_PREVIEW_COUNT', 10))


def set_subtitles(subtitles):
    dao = dao_subtitles.Subtitles()
    result = dao.insert(subtitles)
    if 'subtitles_mongo_document_id' in session:
        dao.remove_by_id(session['subtitles_mongo_document_id'])
    session['subtitles_mongo_document_id'] = str(result.inserted_id)
    dao.remove_documents_older_than(
        result.inserted_id, minutes=REMOVE_OLDER_THAN_MINUTES)


def get_subtitles():
    if 'subtitles_mongo_document_id' not in session:
        raise ValueError("No subtitles found")
    else:
        dao = dao_subtitles.Subtitles()
        subtitles = dao.find_by_id(session['subtitles_mongo_document_id'])
        if subtitles and 'list' in subtitles:
            return [Subtitle.get_instance_from_dict(subtitle)
                    for subtitle in subtitles['list']]
        else:
            raise ValueError("No subtitles found")


def set_preview(subtitles):
    session['preview'] = subtitles[:SUBTITLES_PREVIEW_COUNT]


def get_preview():
    return session['preview'] if 'preview' in session else []


def get_filter(filter_name):
    if filter_name == 'hide_text':
        # TODO Pass actual parameters
        return HideTextFilter(15)
    else:
        raise ValueError("Invalid filter name: '{0}'".format(filter_name))


def get_tuner():
    tuner = Tuner()
    if 'filters' in session:
        for filter_name in session['filters']:
            tuner.add_filter(get_filter(filter_name))
    return tuner
