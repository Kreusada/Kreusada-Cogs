def tick(text):
    return "{} {}".format("\N{BALLOT BOX WITH CHECK}\N{VARIATION SELECTOR-16}", text)


def cross(text):
    return "{} {}".format("\N{CROSS MARK}", text)


def curl(enum):
    return "{{{}}}".format(enum)


def formatenum(enum):
    return enum.replace("__", ".")


def square(text):
    return "[{}]".format(text)


RIGHT_ARROW = "\N{BLACK RIGHTWARDS ARROW}\N{VARIATION SELECTOR-16}"
LEFT_ARROW = "\N{LEFTWARDS BLACK ARROW}\N{VARIATION SELECTOR-16}"
CURRENT_PAGE = "\N{BLACK CIRCLE FOR RECORD}\N{VARIATION SELECTOR-16}"
