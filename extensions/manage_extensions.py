from discord.ext import commands

from shared.utils.permissions import permission_check, Level
from typing import Any


class ManageExtensions(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @permission_check(Level.ADMIN)
    @commands.group(invoke_without_command=True)
    async def extension(self, ctx: commands.Context[Any]) -> None:
        await ctx.reply(f"For managing extensions.\n"
                        f"Must be followed by one of: load, unload, reload, list")

    @permission_check(Level.ADMIN)
    @extension.command()  # type: ignore[attr-defined,untyped-decorator]
    async def unload(self, ctx: commands.Context[Any], extension: str) -> None:
        try:
            await self.bot.unload_extension(extension)
            await ctx.reply("Extension unloaded.")
        except commands.ExtensionNotFound:
            await ctx.reply("That is not a valid extension!")
        except commands.ExtensionNotLoaded:
            await ctx.reply("That extension is not loaded.")

    @permission_check(Level.ADMIN)
    @extension.command()  # type: ignore[attr-defined,untyped-decorator]
    async def load(self, ctx: commands.Context[Any], extension: str) -> None:
        try:
            await self.bot.load_extension(extension)
            await ctx.reply("Extension loaded.")
        except commands.ExtensionNotFound:
            await ctx.reply("That is not a valid extension!")
        except commands.ExtensionAlreadyLoaded:
            await ctx.reply("That extension is already loaded.")
        except commands.NoEntryPointError:
            await ctx.reply("Could not find entry point in that extension.")
        except commands.ExtensionFailed as e:
            print(e)
            await ctx.reply("Extension failed to load.")

    async def reload(self, ctx: commands.Context[Any], extension: str) -> None:
        try:
            await self.bot.reload_extension(extension)
            await ctx.reply("Extension reloaded.")
        except commands.ExtensionNotFound:
            await ctx.reply("That is not a valid extension!")
        except commands.NoEntryPointError:
            await ctx.reply("Could not find entry point in that extension.")
        except commands.ExtensionFailed as e:
            print(e)
            await ctx.reply("Extension failed to load.")
        except commands.ExtensionNotLoaded:
            await ctx.reply("That extension is not loaded.")

    @permission_check(Level.ADMIN)
    @extension.command()  # type: ignore[attr-defined,untyped-decorator]
    async def list(self, ctx: commands.Context[Any]) -> None:
        loaded_extensions = "\n".join(
            [x for x in self.bot.extensions]
        )
        await ctx.reply(f"Currently loaded extensions:\n"
                        f"{loaded_extensions}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ManageExtensions(bot))