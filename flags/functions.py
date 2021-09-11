def square(t):
    return f"[{t}]"


def format_attr(t):
    return t.replace("_", " ").title()


EXCEPTIONS = {"russia": "ru"}
IMAGE_BASE = "https://flagpedia.net/data/flags/w580/{}.png"
SPECIAL_IMAGES = {
    "england": {
        "url": "gb-eng",
        "emoji": "england",
    },
    "wales": {
        "url": "gb-wls",
        "emoji": "wales",
    },
    "scotland": {
        "url": "gb-sct",
        "emoji": "scotland",
    },
    "kosovo": {
        "url": "xk",
        "emoji": "flag_xk",
    },
}
