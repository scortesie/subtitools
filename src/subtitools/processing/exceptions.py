class InvalidSrtFormatError(Exception):
    MSG_IDENTIFIER_MUST_BE_INTEGER = "The identifier must be an integer"
    MSG_TIMESTAMPS_FORMAT = "The timestamps format must be: dd:dd:dd,ddd --> dd:dd:dd,ddd"
    pass
