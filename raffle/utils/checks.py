account_age_checker = lambda x: x < (now - discord_creation_date).days
server_join_age_checker = lambda ctx, x: x < (now - ctx.guild.created_at).days

import datetime

now = datetime.datetime.now()
discord_creation_date = datetime.datetime(2015, 5, 13)

VALID_USER_BADGES = [
    "bug_hunter",
    "bug_hunter_level_2",
    "early_supporter",
    "hypesquad",
    "hypesquad_balance",
    "hypesquad_bravery",
    "hypesquad_brilliance",
    "partner",
    "staff",
    "system",
    "verified_bot_developer",
]
