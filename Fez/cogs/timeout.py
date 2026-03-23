import discord, sqlite3, os, sys
from discord.ext import commands
from shared.utils.permissions import permission_check, Level, has_permission
from shared.utils.misc import getsavedroles, saveroles, is_booster
from shared.config import Config
from discord.ext.commands import MissingRequiredArgument, MemberNotFound

rl_id = Config.json_config['rl_id']

class Timeout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def timeout(self, ctx, member: discord.Member):      
        if any(role in [rl_id["staff"], rl_id["bot"], rl_id["staff-junior"]] for role in ctx.author.roles) or (rl_id["helper"] in member.roles and rl_id["helper"] in ctx.author.roles):
            return await ctx.reply("No")
        
        timeout_id = 332937538648014848

        if ctx.guild.get_role(timeout_id) in member.roles:
            og_roles = await getsavedroles(member.roles)
            await member.edit(roles=og_roles)

            # DELETE REGBAN

            con = sqlite3.connect(os.path.join(sys.path[0], "dbs/regban.db"))
            cur = con.cursor()

            cur.execute("DELETE FROM regban WHERE id = ?", (member.id))
            con.commit()
            con.close()
            await ctx.reply(f"{member.display_name} is now out of time out and roles have been restored.")

            _channel = discord.utils.get(ctx.guild.channels, name="time-out-" + member.id)
            staff_role = discord.utils.get(ctx.guild.roles, id=rl_id["staff"])
            staff_junior_role = discord.utils.get(ctx.guild.roles, id=rl_id["staff-junior"])
            helper_role = discord.utils.get(ctx.guild.roles, id=rl_id["helper"])
            plus_role = discord.utils.get(ctx.guild.roles, rl_id["a-director"]) # lead mod management role

            await _channel.set_permissions(staff_role, view_channel=False)
            await _channel.set_permissions(staff_junior_role, view_channel=False)
            await _channel.set_permissions(helper_role, view_channel=False)

            archive_manager = discord.PermissionOverwrite()
            archive_manager.read_messages = True
            archive_manager.read_message_history = True
            archive_manager.manage_channels = True

            await _channel.set_permissions(plus_role, overwrite=archive_manager)
            await _channel.send(f"<@&{rl_id["staff-alert"]}> This time-out has concluded.")
            await _channel.edit(name=f"closed-{member.id}")
        
        else:
            await saveroles(member)

            timeout_roles = []

            if is_booster(member):
                timeout_roles.append(discord.utils.get(ctx.server.roles, id=580585348371841034))
    
    @timeout.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            return await ctx.reply("No member found with that ID.")
        
        elif isinstance(error, MissingRequiredArgument):
            return await ctx.reply("Please provide a user ID.")

async def setup(bot):
    await bot.add_cog(Timeout(bot))