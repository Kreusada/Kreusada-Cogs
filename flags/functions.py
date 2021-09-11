def square(t):
    return f"[{t}]"


def format_attr(t):
    return t.replace("_", " ").title()


EXCEPTIONS = {"russia": "ru"}
IMAGE_BASE = "https://flagpedia.net/data/flags/w580/{}.png"
SPECIAL_IMAGES = {
    "england": "gb-eng",
    "wales": "gb-wls",
    "scotland": "gb-sct",
    "kosovo": "xk",
}
