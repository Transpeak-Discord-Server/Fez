import discord
from discord import app_commands
from discord.ext import commands

from shared.utils.permissions import Level, permission_check


class ManageExtensions(app_commands.Group):

    def __init__(self, bot: commands.Bot):
        super().__init__(name="extension")
        self.bot = bot

    @app_commands.command()
    @permission_check(Level.ADMIN)
    async def unload(self, interaction: discord.Interaction[commands.Bot], extension: str) -> None:
        try:
            await self.bot.unload_extension(extension)
            await interaction.response.send_message("Extension unloaded.")
        except commands.ExtensionNotFound:
            await interaction.response.send_message("That is not a valid extension!")
        except commands.ExtensionNotLoaded:
            await interaction.response.send_message("That extension is not loaded.")

    @app_commands.command()
    @permission_check(Level.ADMIN)
    async def load(self, interaction: discord.Interaction[commands.Bot], extension: str) -> None:
        try:
            await self.bot.load_extension(extension)
            await interaction.response.send_message("Extension loaded.")
        except commands.ExtensionNotFound:
            await interaction.response.send_message("That is not a valid extension!")
        except commands.ExtensionAlreadyLoaded:
            await interaction.response.send_message("That extension is already loaded.")
        except commands.NoEntryPointError:
            await interaction.response.send_message("Could not find entry point in that extension.")
        except commands.ExtensionFailed as e:
            print(e)
            await interaction.response.send_message("Extension failed to load.")

    @app_commands.command()
    @permission_check(Level.ADMIN)
    async def reload(self, interaction: discord.Interaction[commands.Bot], extension: str) -> None:
        try:
            await self.bot.reload_extension(extension)
            await interaction.response.send_message("Extension reloaded.")
        except commands.ExtensionNotFound:
            await interaction.response.send_message("That is not a valid extension!")
        except commands.NoEntryPointError:
            await interaction.response.send_message("Could not find entry point in that extension.")
        except commands.ExtensionFailed as e:
            print(e)
            await interaction.response.send_message("Extension failed to load.")
        except commands.ExtensionNotLoaded:
            await interaction.response.send_message("That extension is not loaded.")

    @app_commands.command()
    @permission_check(Level.ADMIN)
    async def list(self, interaction: discord.Interaction[commands.Bot]) -> None:
        loaded_extensions = "\n".join(
            [x for x in self.bot.extensions]
        )
        await interaction.response.send_message(f"Currently loaded extensions:\n"
                                                f"{loaded_extensions}")

async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(ManageExtensions(bot))
    await bot.tree.sync()