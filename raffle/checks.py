account_age_checker = lambda x: x < (now - discord_creation_date).days
join_age_checker = lambda ctx, x: x < (now - ctx.guild.created_at).days

import datetime
now = datetime.datetime.now()
discord_creation_date = datetime.datetime(2015, 5, 13)