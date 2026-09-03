import dataclasses
from typing import Any, cast

import discord
from discord import TextChannel, app_commands, DMChannel, Guild, Role, CategoryChannel
from discord.ext import commands

from shared.config import Config
from shared.utils.misc import get_member_or_user
from shared.utils.permissions import permission_check, Level

config = Config.json_config


@dataclasses.dataclass
class TicketMessageDetails:
    server: discord.Guild
    channel: TextChannel
    user: discord.User | discord.Member
    staff_member: discord.User | discord.Member
    message: str


class ContactStaff(commands.GroupCog):
    ticket_channels: list[TextChannel]
    server: Guild
    staff_role: Role
    bot_role: Role
    staff_alert_role: Role
    ticket_category: CategoryChannel

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self) -> None:
        server = await self.bot.fetch_guild(config['server_id'])
        if server is None:
            raise ValueError("Could not find server from server_id in config")
        self.server = server

        staff_role = self.server.get_role(config['rl_id']['staff'])
        bot_role = self.server.get_role(config['rl_id']['bot'])
        staff_alert_role = self.server.get_role(config['rl_id']['staff-alert'])
        if staff_role is None or bot_role is None or staff_alert_role is None:
            raise ValueError("Could not find roles from role ids in config")
        self.staff_role = staff_role
        self.bot_role = bot_role
        self.staff_alert_role = staff_alert_role

        tickets_category = await self.server.fetch_channel(config['cat_id']['tickets'])
        if not isinstance(tickets_category, CategoryChannel):
            raise ValueError("Could not find tickets category from id in config")
        self.ticket_category = tickets_category

        server_channels = await self.server.fetch_channels()
        self.ticket_channels = cast(list[TextChannel], [
            x for x in server_channels
            if isinstance(x, TextChannel)
               and x.category == self.ticket_category
        ])
        await self.bot.tree.sync()

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command("contact-staff")

    async def get_user(self, server: discord.Guild, channel: TextChannel) -> discord.Member | discord.User | None:
        description = channel.topic
        if description is None: return None

        description_words = description.split(' ')
        if len(description_words) < 3: return None
        if not description_words[2].isdigit(): return None
        user_id = int(description_words[2])

        return await get_member_or_user(server, self.bot, user_id)

    @app_commands.command()
    @app_commands.describe(message="Your initial message to staff")
    async def contact_staff(self, interaction: discord.Interaction[Any], message: str) -> None:

        ticket_name = interaction.user.name
        if any(x.name == ticket_name for x in self.ticket_channels):
            await interaction.response.send_message(
                "You already have a ticket open with staff. Please message me in DMs to contact staff!")
            return None

        channel = await self.server.create_text_channel(name=ticket_name, category=self.ticket_category,
                                                        topic=f"ModMail Ticket {interaction.user.id} (Please do not change this)")
        self.ticket_channels.append(channel)

        await channel.set_permissions(self.staff_role, view_channel=True, send_messages=True)
        await channel.set_permissions(self.bot_role, view_channel=True, send_messages=True, manage_channels=True)

        msg_embed = discord.Embed(
            title="New Ticket",
            description=interaction.message,
            colour=discord.Colour.green()
        )
        msg_embed.set_author(name=f"{interaction.user.name} | {interaction.user.id}",
                             icon_url=interaction.user.display_avatar.url)
        await channel.send(self.staff_alert_role.mention, embed=msg_embed)

        await interaction.response.send_message("Ticket opened. Staff will be with you shortly!")
        return None

    @staticmethod
    async def send_msg_received(message: str, author: discord.User | discord.Member,
                                send_in: discord.abc.Messageable) -> None:
        msg_embed = discord.Embed(
            title="Message Received",
            description=message,
            colour=discord.Colour.green()
        )
        msg_embed.set_author(name=author.name, icon_url=author.display_avatar.url)
        await send_in.send(embed=msg_embed)

    @staticmethod
    async def send_msg_sent(message: str, author: discord.User | discord.Member,
                            send_in: discord.abc.Messageable) -> None:
        msg_embed = discord.Embed(
            title="Message Sent",
            description=message,
            colour=discord.Colour.orange()
        )
        msg_embed.set_author(name=author.name, icon_url=author.display_avatar.url)
        await send_in.send(embed=msg_embed)

    async def get_msg_details(self, ctx: commands.Context[Any], args: tuple[str, ...]) -> TicketMessageDetails | None:
        server = ctx.guild
        if server is None:
            await ctx.reply("This command can only be used within Transpeak!")
            return None

        channel = ctx.channel
        if not isinstance(channel, TextChannel): return None

        category = channel.category
        if category is None or category != self.ticket_category: return None

        user = await self.get_user(server, channel)
        if user is None:
            await ctx.reply("User not found.")
            return None

        staff_member = ctx.author
        message = " ".join(args)
        return TicketMessageDetails(server, channel, user, staff_member, message)

    @commands.command()
    @permission_check(Level.STAFF)
    async def reply(self, ctx: commands.Context[Any], *args: str) -> None:

        ticket_details = await self.get_msg_details(ctx, args)
        if not ticket_details: return None

        try:
            await self.send_msg_received(ticket_details.message, ticket_details.staff_member, ticket_details.user)
        except discord.Forbidden:
            await ctx.reply("User cannot be messaged.")
            return None
        except discord.NotFound:
            await ctx.reply("User not found.")
            return None
        except Exception as e:
            await ctx.reply(f"Error sending message: {e}")

        await self.send_msg_sent(ticket_details.message, ticket_details.staff_member, ctx.channel)

        return None

    @commands.command()
    @permission_check(Level.STAFF)
    async def close(self, ctx: commands.Context[Any], *args: str) -> None:

        ticket_details = await self.get_msg_details(ctx, args)
        if not ticket_details: return None

        await ctx.reply("Closing ticket...")

        # TODO: archive and delete ticket channel

        return None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:

        channel = message.channel
        if not isinstance(channel, DMChannel): return None

        user = message.author
        ticket_channel_matches = [x for x in self.ticket_channels if x.name == user.name]
        if not ticket_channel_matches: return None

        # two tickets can't have the same name, as per this code's logic
        ticket_channel = ticket_channel_matches[0]
        await self.send_msg_received(message.content, message.author, ticket_channel)
        await self.send_msg_sent(message.content, message.author, user)

        return None

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ContactStaff(bot))
    return None