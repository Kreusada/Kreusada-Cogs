def tick(text):
    return "{} {}".format("\N{BALLOT BOX WITH CHECK}\N{VARIATION SELECTOR-16}", text)

def cross(text):
    return "{} {}".format("\N{CROSS MARK}", text)

def curl(enum):
    return "{{{}}}".format(enum)

def formatenum(enum):
    return enum.replace("__", ".")