from redbot.core.commands import Context

from ..log import log
from ..mixins.abc import RaffleMixin


class CleanupHelpers(RaffleMixin):
    """Various utilities to prevent stale dictionary values"""

    async def clean_raffles(self, ctx: Context) -> None:
        async with self.config.guild(ctx.guild).raffles() as r:

            updates = {}

            for k, v in list(r.items()):

                getter = v.get("owner")
                if not ctx.guild.get_member(getter):
                    del r[k]
                    updates["owner"] = True

                getter = v.get("entries")
                for userid in getter:
                    if not ctx.guild.get_member(userid):
                        getter.remove(userid)
                        updates["entries"] = True

                getter = v.get("prevented_users", None)
                if getter:
                    for userid in getter:
                        if not ctx.guild.get_member(userid):
                            getter.remove(userid)
                            updates["prevented_users"] = True

                getter = v.get("allowed_users", None)
                if getter:
                    for userid in getter:
                        if not ctx.guild.get_member(userid):
                            getter.remove(userid)
                            updates["allowed_users"] = True

                getter = v.get("roles_needed_to_enter", None)
                if getter:
                    for roleid in getter:
                        if not ctx.guild.get_role(roleid):
                            getter.remove(roleid)
                            updates["roles_needed_to_enter"] = True

        return any(updates.values())

    @property
    def clean_guild_raffles(self):
        return self.clean_raffles

    async def initialize(self):
        all_guilds = await self.config.all_guilds()
        changed_guilds = []
        for g in all_guilds.keys():
            gobj = self.bot.get_guild(g)
            if not gobj:
                continue
            raffles = all_guilds[g]["raffles"]
            for r in raffles.keys():
                IDS = {}
                if raffles[r] and "roles" in r:
                    IDS[r] = "get_role"
                elif raffles[r] and "users" in r:
                    IDS[r] = "get_member"
                else:
                    continue

                if not gobj.get_member(raffles[r]["owner"]):
                    del raffles[r]
                    changed_guilds.append(g)

                for k, v in IDS.items():
                    for obj in raffles[k]:
                        if not getattr(gobj, f"get_{v}")(obj):
                            del raffles[k][obj]
                            changed_guilds.append(g)
            if changed_guilds:
                await self.config.guild(gobj).raffles.set(raffles)
        log.info("Raffles cleaned up across %s guilds" % len(all_guilds.keys()))
        if changed_guilds:
            log.info(
                "%s guild raffle dictionaries were edited to remove deleted/unknown users and roles"
                % len(changed_guilds)
            )

    async def clean_singular_raffle(self, ctx: Context, raffle: str) -> None:
        async with self.config.guild(ctx.guild).raffles() as r:

            updates = {}
            raffle_data = r[raffle]

            getter = raffle_data.get("owner")
            if not ctx.guild.get_member(getter):
                del r[raffle][getter]
                updates["owner"] = True

            getter = raffle_data.get("entries")
            for userid in getter:
                if not ctx.guild.get_member(userid):
                    getter.remove(userid)
                    updates["entries"] = True

            getter = raffle_data.get("prevented_users", None)
            if getter:
                for userid in getter:
                    if not ctx.guild.get_member(userid):
                        getter.remove(userid)
                        updates["prevented_users"] = True

            getter = raffle_data.get("allowed_users", None)
            if getter:
                for userid in getter:
                    if not ctx.guild.get_member(userid):
                        getter.remove(userid)
                        updates["allowed_users"] = True

            getter = raffle_data.get("roles_needed_to_enter", None)
            if getter:
                for roleid in getter:
                    if not ctx.guild.get_role(roleid):
                        getter.remove(roleid)
                        updates["roles_needed_to_enter"] = True

        return any(updates.values())
