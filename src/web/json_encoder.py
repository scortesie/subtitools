from flask.json import JSONEncoder

from subtitools.processing.subtitle import Subtitle


class SubtitoolsJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Subtitle):
            return obj.to_json()
        else:
            JSONEncoder.default(self, obj)
