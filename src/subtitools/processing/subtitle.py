"""
Data structures used to represent subtitles.
"""

import json


class Subtitle(object):
    def __init__(self, identifier=None,
                 timestamp_begin=None, timestamp_end=None, text=None):
        self.identifier = identifier
        self.timestamp_begin = timestamp_begin
        self.timestamp_end = timestamp_end
        self.text = text

    def __str__(self):
        return '{0}\n{1} --> {2}\n{3}'.format(self.identifier,
                                              self.timestamp_begin,
                                              self.timestamp_end,
                                              self.text.encode('utf-8'))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def get_instance_from_dict(_dict):
        return Subtitle(
            _dict['identifier'],
            _dict['timestamp_begin'],
            _dict['timestamp_end'],
            _dict['text'])

    @staticmethod
    def get_instance_from_json(json_string):
        return Subtitle.get_instance_from_dict(json.loads(json_string))
