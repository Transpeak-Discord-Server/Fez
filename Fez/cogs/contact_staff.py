import dataclasses
import io
import textwrap
from datetime import datetime
from typing import Any, cast

import discord
from discord import TextChannel, app_commands, DMChannel, Guild, Role, CategoryChannel
from discord.ext import commands
from discord.ext.commands import Context

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
    ticket_log_channel: TextChannel

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

        ticket_log_channel = await self.server.fetch_channel(config['ch_id']['ticket-log'])
        if not isinstance(ticket_log_channel, TextChannel):
            raise ValueError("Could not find ticket log channel from id in config")
        self.ticket_log_channel = ticket_log_channel

        self.ticket_channels = []

        await self.bot.tree.sync()

    def load_ticket_channels(self) -> None:
        tickets_category = self.server.get_channel(config['cat_id']['tickets'])
        if not isinstance(tickets_category, CategoryChannel):
            raise ValueError("Could not find tickets category from id in config")
        self.ticket_category = tickets_category

        self.ticket_channels = self.ticket_category.text_channels

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
            description=message,
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

    def get_ticket_channel(self, user: discord.User | discord.Member) -> discord.TextChannel | None:
        if not self.ticket_channels: self.load_ticket_channels()
        for channel in self.ticket_channels:

            topic = channel.topic
            if topic is None: return None

            topic_split = topic.split(" ")
            if len(topic_split) < 3: return None

            channel_user_id = topic_split[2]
            if not channel_user_id.isdigit(): return None
            if user.id == int(channel_user_id): return channel
        return None

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

    @staticmethod
    async def msg_to_string(ctx: Context[Any], message: discord.Message) -> str | None:
        message_author = f"{message.author.name} ({message.author.id})"

        embed_str: str | None = None
        if len(message.embeds) != 0:
            embed = message.embeds[0]
            if embed.title == "Message sent": return None
            embed_str = embed.description

        reply = ""
        if message.reference is not None and message.reference.message_id is not None:
            reply_message = await ctx.fetch_message(message.reference.message_id)
            reply_message_user = reply_message.author.name
            shortened_reply_message = textwrap.shorten(reply_message.content, 10, placeholder="...")
            reply = f" (In reply to @{reply_message_user}: \"{shortened_reply_message}\")"

        message_content = message.content if not embed_str else f"Message received - {embed_str}"

        return f"{message_author}{reply}: {message_content}"

    @commands.command()
    @permission_check(Level.STAFF)
    async def close(self, ctx: commands.Context[Any], *args: str) -> None:

        ticket_details = await self.get_msg_details(ctx, args)
        if not ticket_details: return None

        await ctx.reply("Closing ticket...")

        ticket_messages = ticket_details.channel.history(oldest_first=True)
        ticket_str = ""
        async for message in ticket_messages:
            message_str = await self.msg_to_string(ctx, message)
            if message_str is not None: ticket_str += f"{message_str}\n"

        ticket_bytes = ticket_str.encode("utf-8")
        ticket_file = discord.File(io.BytesIO(ticket_bytes), filename="ticket_log.txt")

        ticket_embed = discord.Embed(
            title="Ticket Closed",
            timestamp=datetime.now(),
            description=f"**Reason:** {" ".join(args)}"
        )
        ticket_embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        ticket_embed.set_footer(text=f"{ticket_details.user.name} | {ticket_details.user.id}", icon_url=ticket_details.user.display_avatar.url)

        await self.ticket_log_channel.send(file=ticket_file, embed=ticket_embed)
        await ticket_details.channel.delete(reason=f"Ticket closed by {ctx.author.name}")

        return None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:

        channel = message.channel
        if not isinstance(channel, DMChannel): return None

        user = message.author

        ticket_channel = self.get_ticket_channel(user)
        if ticket_channel is None: return None

        await self.send_msg_received(message.content, message.author, ticket_channel)
        await self.send_msg_sent(message.content, message.author, user)

        return None

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ContactStaff(bot))
    return None