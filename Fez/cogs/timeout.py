import discord, sqlite3, os, sys
from discord.ext import commands
from shared.utils.permissions import permission_check, Level, has_permission
from shared.utils.misc import getsavedroles, saveroles, is_booster
from shared.config import Config
from discord.ext.commands import MissingRequiredArgument, MemberNotFound

rl_id = Config.json_config['rl_id']
identities_for_cmd = Config.json_config["identities_for_cmd"]

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

            if is_booster(ctx.guild, member):
                timeout_roles.append(discord.utils.get(ctx.guild.roles, id=580585348371841034))
            
            premium_roles = [discord.utils.get(ctx.guild.roles, id=role_id) for role_id in [942905231417688118, 942905807480180736, 942905672402624563, 943263055675023391]]

            if any(role in premium_roles for role in member.roles):
                intersected_roles = [role for role in premium_roles if role in member.roles]

                for role in intersected_roles:
                    timeout_roles.append(role)
                
                timeout_roles.append(discord.utils.get(ctx.guild.roles, id=timeout_id))
                timeout_roles.extend([role for role in member.roles if role.name in identities_for_cmd["transfemale_pronouns"] + identities_for_cmd["transmale_pronouns"] + identities_for_cmd["nonbinary_pronouns"]])
                await member.edit(roles=timeout_roles)

                # everyone = discord.PermissionOverwrite()
                # everyone.send_messages = False
                # everyone.read_messages = False

                # normal_perms = discord.PermissionOverwrite()
                # normal_perms.send_messages = True
                # normal_perms.read_messages = True
                # normal_perms.read_message_history = True

                # pk_perms = discord.PermissionOverwrite()
                # pk_perms.send_messages = True
                # pk_perms.read_messages = True

                # manage = discord.PermissionOverwrite()
                # manage.manage_channels = True
                # manage.send_messages = True
                # manage.read_messages = True
                # manage.read_message_history = True

                everyone = ctx.guild.default_role
                staff_role = discord.utils.get(ctx.guild.roles, id=rl_id["staff"])
                staff_junior_role = discord.utils.get(ctx.guild.roles, id=rl_id["staff-junior"])
                helper_role = discord.utils.get(ctx.guild.roles, id=rl_id["helper"])
                admin_role = discord.utils.get(ctx.guild.roles, id=rl_id["admin"])
                bot_role = discord.utils.get(ctx.guild.roles, id=rl_id["bot"])
                pk = discord.utils.get(ctx.guild.members, id=466378653216014359)

                everyone_perms = discord.PermissionOverwrite(send_messages=False, read_messages=False)
                normal_perms = discord.PermissionOverwrite(send_messages=True, read_messages=True, read_message_history=True)
                manage_perms = discord.PermissionOverwrite(manage_channels=True, send_messages=True, read_messages=True, read_message_history=True)

                overwrites = {
                    everyone: everyone_perms,
                    staff_role: normal_perms,
                    staff_junior_role: normal_perms,
                    helper_role: normal_perms,
                    admin_role: manage_perms,
                    bot_role: manage_perms,
                    pk: manage_perms
                }
    
    @timeout.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            return await ctx.reply("No member found with that ID.")
        
        elif isinstance(error, MissingRequiredArgument):
            return await ctx.reply("Please provide a user ID.")

async def setup(bot):
    await bot.add_cog(Timeout(bot))