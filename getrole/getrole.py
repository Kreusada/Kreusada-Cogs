    @commands.group()
    async def role(self, ctx):
        """Base role command
        This allows you to buy certain roles for credits"""

    @role.command(name="add")
    @checks.admin()
    async def _add(self, ctx, role: discord.Role, cost: int = 3000):
        """Add a purchasable role"""
        await self.config.guild(ctx.guild).roles.set_raw(role, value=cost)
        await ctx.send("That role can now be bought for {}".format(cost))

    @role.command(aliases=["del", ])
    @checks.admin()
    async def remove(self, ctx, *, role):
        try:
            await self.config.guild(ctx.guild).roles.clear_raw(role)
            await ctx.send("Removed that role from the store")
        except KeyError:
            await ctx.send("I couldn't find that role")

    @role.command()
    async def buy(self, ctx, *, role: discord.Role):
        """Buy a role with credits"""
        try:
            role_cost = await self.config.guild(ctx.guild).roles.get_raw(role)
        except KeyError:
            return await ctx.send("I could not find that role!")

        if await bank.can_spend(ctx.author, role_cost):
            try:
                await ctx.author.add_roles(role)
                await bank.withdraw_credits(ctx.author, role_cost)
                await ctx.send("You have sucessfully bought that role!")
            except discord.Forbidden:
                await ctx.send("I could not attach that role!")
