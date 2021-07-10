import logging

log = logging.getLogger("red.core.RLL")
socket_log = logging.getLogger("red.core.RLL.socket")
socket_log.setLevel(logging.INFO)

ws_discord_log = logging.getLogger("red.Audio.WS.discord")
ws_ll_log = logging.getLogger("red.Audio.WS.LLServer")
ws_rll_log = logging.getLogger("red.Audio.WS.RLL")


def set_logging_level(level=logging.INFO):
    log.setLevel(level)
    ws_discord_log.setLevel(level)
    ws_ll_log.setLevel(level)
    ws_rll_log.setLevel(level)
