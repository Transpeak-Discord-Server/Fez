from discord.ext import commands

from shared.utils.permissions import permission_check, Level, has_permission

class Ban(commands.Cog):

    flags = ["-nd", "-d"]

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @permission_check(Level.STAFF)
    async def ban(self, ctx, *args: str):
        if not args: return None

        if not args[0].isdigit():
            return await ctx.send("Please provide a valid user ID.")

        user = self.bot.get_user(int(args[0]))
        if not user:
            return await ctx.send("User not found.")

        if has_permission(ctx.author, Level.HELPER):
            return await ctx.send("You cannot ban a staff member.")

        reason = args[1:]
        if not reason:
            return await ctx.send("Please provide a reason.")

        ban_flag = None
        for flag in reason:
            if flag in self.flags:
                ban_flag = flag
                reason = reason.replace(flag, "")
        if not ban_flag:
            return await ctx.send("No ban flag found. Please use -nd or -d.")

        " ".join(reason)

        if ban_flag == "-nd":


async def setup(bot):
    await bot.add_cog(Ban(bot))

