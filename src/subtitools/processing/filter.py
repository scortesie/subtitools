import re
import logging

from subtitools.processing.subtitle import Subtitle

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Filter(object):
    def __init__(self):
        pass

    def filter(self, subtitle):
        raise NotImplementedError()


class HideTextFilter(Filter):
    def __init__(self, percentage_to_hide):
        Filter.__init__(self)
        self.re_word = re.compile('\w+', re.UNICODE)
        self.percentage_to_hide = int(percentage_to_hide)
        if self.percentage_to_hide not in range(1, 101):
            raise ValueError("Percentage must be a number between 1 and 100")

    def hide_word(self, word):
        return u'_' * len(word)

    def filter(self, subtitle):
        subtitle_text = subtitle.text
        subtitle_text_filtered = u''
        text_current_char_index = 0
        text_current_word_position = 0
        for match in self.re_word.finditer(subtitle_text):
            text_current_word_str = match.group()
            text_current_word_span = match.span()
            subtitle_text_filtered += subtitle_text[text_current_char_index:text_current_word_span[0]]
            if text_current_word_position % int(100 / self.percentage_to_hide) == 0:
                text_current_word_str = self.hide_word(text_current_word_str)
            subtitle_text_filtered += text_current_word_str
            text_current_char_index = text_current_word_span[1]
            text_current_word_position += 1
        subtitle_text_filtered += subtitle_text[text_current_char_index:]
        return Subtitle(subtitle.identifier,
                        subtitle.timestamp_begin,
                        subtitle.timestamp_end,
                        subtitle_text_filtered)
