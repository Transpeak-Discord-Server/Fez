import discord
from discord import app_commands
from discord.ext import commands

from shared.database import data
from shared.database.UserDAO import UserDAO
from shared.database.__main__ import Database, get_database
from shared.utils.misc import format_time, require_server, get_week
from shared.utils.permissions import permission_check, Level


class UserGroup(app_commands.Group):

    database: Database

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.name = "user"
        self.database = get_database()

    @staticmethod
    async def build_info_embed(server: discord.Guild, user: discord.User | discord.Member, db_data: data.User | None, msg_count_week: int, msg_count_week_previous: int, wl: str | None, sc: str | None) -> discord.Embed:
        embed_description = (f"{user.mention}\n"
                             f"**Created account:** {format_time(user.created_at, "f")}\n")
        if isinstance(user, discord.Member):
            embed_description += (f"**Joined server:** {format_time(user.joined_at, "f")}\n"
                                  f"**Status:** {user.status}\n")
        if db_data is not None:
            embed_description += (f"**Message count:** {db_data.message_count}\n"
                                  f"**Message count this week:** {msg_count_week}\n"
                                  f"**Message count last week:** {msg_count_week_previous}\n"
                                  f"**Under 18:** {db_data.under_18}\n"
                                  f"**Registration banned:** {db_data.reg_banned}\n")

        if isinstance(user, discord.User):
            try:
                await server.fetch_ban(user)
                banned = True
            except discord.NotFound:
                banned = False
            embed_description += f"**Banned:** {"Yes" if banned else "No"}\n"

        embed = discord.Embed(
            title="User info",
            description=embed_description,
            colour=discord.Colour.green() if isinstance(user, discord.Member) else discord.Colour.red()
        )
        embed.set_author(name=f"{user.display_name} ({user.id})", icon_url=user.display_avatar.url)

        if isinstance(user, discord.Member):
            roles = [x.name for x in user.roles]
            embed.add_field(name="Roles", value=", ".join(roles), inline=False)

        if wl:
            embed.add_field(name="Watchlist", value=wl, inline=False)
        if sc:
            embed.add_field(name="Special Considerations", value=sc, inline=False)

        if db_data and db_data.last_message:
            embed.add_field(name="Last message", value=f"\"{db_data.last_message}\"", inline=False)

        return embed

    @app_commands.command()
    @permission_check(Level.STAFF)
    async def info(self, interaction: discord.Interaction[commands.Bot], user: discord.User | discord.Member | None) -> None:
        if user is None: user = interaction.user

        server = await require_server(interaction)
        if not server: return

        async with self.database.get_session() as session:
            user_dao = UserDAO(session)
            user_db_info = await user_dao.get_user_info(user.id)
            msg_count_week = await user_dao.get_message_count_week(user.id)
            msg_count_previous_week = await user_dao.get_message_count_week(user.id, get_week() - 1)
            wl = await user_dao.get_watchlist(user.id)
            sc = await user_dao.get_special_considerations(user.id)

        embed = await self.build_info_embed(server, user, user_db_info, msg_count_week, msg_count_previous_week, wl, sc)

        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    @permission_check(Level.STAFF)
    async def set_watchlist(self, interaction: discord.Interaction[commands.Bot], user: discord.User | discord.Member, wl: str) -> None:
        async with self.database.get_session() as session:
            user_dao = UserDAO(session)
            await user_dao.set_watchlist(user.id, wl)
        await interaction.response.send_message("Watchlist set.")

    @app_commands.command()
    @permission_check(Level.STAFF)
    async def set_special_considerations(self, interaction: discord.Interaction[commands.Bot], user: discord.User | discord.Member, sc: str) -> None:
        async with self.database.get_session() as session:
            user_dao = UserDAO(session)
            await user_dao.set_special_considerations(user.id, sc)
        await interaction.response.send_message("Special considerations set.")

    @app_commands.command()
    @permission_check(Level.STAFF)
    async def reg_ban(self, interaction: discord.Interaction[commands.Bot], user: discord.User | discord.Member) -> None:
        async with self.database.get_session() as session:
            user_dao = UserDAO(session)
            await user_dao.reg_ban(user.id)
        await interaction.response.send_message("User has been banned from self-registration.")

    @app_commands.command()
    @permission_check(Level.STAFF)
    async def un_reg_ban(self, interaction: discord.Interaction[commands.Bot], user: discord.User | discord.Member) -> None:
        async with self.database.get_session() as session:
            user_dao = UserDAO(session)
            await user_dao.un_reg_ban(user.id)
        await interaction.response.send_message("User is no longer registration banned.")

    @app_commands.command()
    @permission_check(Level.STAFF)
    async def set_under_18(self, interaction: discord.Interaction[commands.Bot], user: discord.User | discord.Member, under_18: bool) -> None:
        async with self.database.get_session() as session:
            user_dao = UserDAO(session)
            await user_dao.set_user_over_18(user.id, under_18)
        await interaction.response.send_message("User under 18 value set.")

async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(UserGroup(bot))