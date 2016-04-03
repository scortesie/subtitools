"""
Data structures used to represent subtitles.
"""

import json


class Subtitle(object):
    def __init__(self, identifier=None, timestamp_begin=None, timestamp_end=None, text=None):
        self.identifier = identifier
        self.timestamp_begin = timestamp_begin
        self.timestamp_end = timestamp_end
        self.text = text

    def __str__(self):
        return '{0}\n{1} --> {2}\n{3}'.format(str(self.identifier),
                                              str(self.timestamp_begin),
                                              str(self.timestamp_end),
                                              str(self.text))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def get_instance_from_json(json_string):
        json_data = json.loads(json_string)
        return Subtitle(
            json_data['identifier'],
            json_data['timestamp_begin'],
            json_data['timestamp_end'],
            json_data['text'])
