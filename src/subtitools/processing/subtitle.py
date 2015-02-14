"""
Data structures used to represent subtitles.
"""


class Subtitle(object):
    def __init__(self, identifier=None, timestamp_begin=None, timestamp_end=None, text=None):
        self.identifier = identifier
        self.timestamp_begin = timestamp_begin
        self.timestamp_end = timestamp_end
        self.text = text
