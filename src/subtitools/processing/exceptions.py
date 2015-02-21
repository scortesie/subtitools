class InvalidSrtFormatError(Exception):
    MSG_IDENTIFIER_MUST_BE_INTEGER = "The identifier must be an integer"
    MSG_TIMESTAMPS_FORMAT = "The timestamps format must be: dd:dd:dd,ddd --> dd:dd:dd,ddd"
    MSG_TEXT_MUST_HAVE_ONE_LINE = "The text must have at least one line"
    MSG_SUBTITLE_MUST_END_WITH_NEWLINE = "The subtitle must end with newline"
