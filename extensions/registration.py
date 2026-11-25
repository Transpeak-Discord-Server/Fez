from pathlib import Path
from typing import Any, Optional

import discord
from discord import app_commands, Interaction
from discord import ui
from discord.ext import commands

from extensions import contact_staff
from shared.config import Config
from shared.utils.errors import ConfigError
from shared.utils.misc import require_server
from shared.utils.permissions import permission_check, Level

config = Config.json_config

messages_folder = Path(__file__).parent.parent / "shared" / "messages" / "registration"
entry_reg_message_location = messages_folder / "entry_reg"
check_rules_message_location = messages_folder / "check_rules"
wrong_word_message_location = messages_folder / "wrong_word"
pick_identities_message_location = messages_folder / "pick_identities"

entry_reg_message: str = "didnt load :("
check_rules_message: str = "didnt load :("
wrong_word_message: str = "didnt load :("
pick_identities_message: str = "didnt load :("


answer = "Grapes"

async def create_ticket(interaction: discord.Interaction[Any]) -> None:
    contact_extension = interaction.client.get_cog("ContactStaff")
    if not isinstance(contact_extension, contact_staff.ContactStaff):
        await interaction.response.send_message(
            "Something went wrong! You can try using `/modmail open-ticket`, and if that doesn't work, DM a staff member.")
        return
    await contact_extension.contact_staff.callback(contact_extension, interaction,  # type: ignore[call-arg,arg-type]
                                                   "['Contact staff' button interaction from registration]")

class RegistrationIdentitiesModal(discord.ui.Modal):
    title = "Submit Identity Roles"
    message: ui.TextDisplay[ui.LayoutView] = ui.TextDisplay("Please enter your selected roles here, separated by spaces or commas.")
    identities_input: ui.Label[ui.view.BaseView] = discord.ui.Label(text="Enter your selection here", component=discord.ui.TextInput(placeholder="Your selection (separated by spaces or commas)..."))

    async def on_submit(self, interaction: Interaction[discord.Client]) -> None:
        await interaction.response.send_message("registration stuff")

class RegistrationIdentities(discord.ui.LayoutView):

    message: ui.TextDisplay[ui.LayoutView] = discord.ui.TextDisplay("placeholder")
    button_row: ui.ActionRow[ui.LayoutView] = ui.ActionRow()

    def __init__(self, *, timeout: Optional[float] = 180.0):
        super().__init__(timeout=timeout)
        self.message.content = pick_identities_message

    @button_row.button(label="Enter roles...")
    async def submit_button(self, interaction: discord.Interaction[commands.Bot], button: discord.ui.Button[Any]) -> None:
        await interaction.response.send_modal(RegistrationIdentitiesModal())

    @button_row.button(label="Contact staff")
    async def on_submit(self, interaction: discord.Interaction[commands.Bot], button: discord.ui.Button[Any]) -> None:
        await create_ticket(interaction)

class RegistrationSecretModal(discord.ui.Modal):

    title = "Registration Question"
    question_text: ui.TextDisplay[ui.LayoutView] = ui.TextDisplay("Thank you for reading our rules! Please enter the secret word below.")
    question_field: ui.Label[ui.view.BaseView] = ui.Label(text='Secret Word', component=ui.TextInput())

    async def on_submit(self, interaction: discord.Interaction[discord.Client]) -> None:
        member = interaction.user

        if self.question_field.component.value == answer:  # type: ignore[attr-defined]
            await interaction.response.send_message(view=RegistrationIdentities())
        else:
            await member.send(view=RegistrationRules(message=wrong_word_message))



class RegistrationRules(discord.ui.LayoutView):

    message: ui.TextDisplay[ui.LayoutView] = ui.TextDisplay("Placeholder")
    button_row: ui.ActionRow[ui.LayoutView] = ui.ActionRow()

    def __init__(self, *, timeout: Optional[float] = 180.0, message: Optional[str] = None):
        super().__init__(timeout=timeout)
        if message is not None:
            self.message.content = message
        else:
            self.message.content = check_rules_message

    @button_row.button(label="I have read the rules.")
    async def read_rules(self, interaction: discord.Interaction[commands.Bot], button: ui.Button[Any]) -> None:
        await interaction.response.send_modal(RegistrationSecretModal())

    @button_row.button(label="Contact staff")
    async def on_submit(self, interaction: discord.Interaction[commands.Bot], button: discord.ui.Button[Any]) -> None:
        await create_ticket(interaction)

class RegistrationBegin(discord.ui.View):

    @discord.ui.button(label='Begin Registration')
    async def begin_registration(self, interaction: discord.Interaction[commands.Bot], button: discord.ui.Button[Any]) -> None:
        member = interaction.user
        if not isinstance(member, discord.Member):
            await interaction.response.send_message("Something went wrong! Please try again or contact a member of staff.", ephemeral=True)
            return

        await member.send(view = RegistrationRules())


class Registration(commands.GroupCog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command()
    @permission_check(Level.ADMIN)
    async def setup(self, interaction: discord.Interaction[commands.Bot]) -> None:
        server = await require_server(interaction)
        if not server: return

        entry_reg_channel = server.get_channel(config['ch_id']['#entry-reg'])
        if not isinstance(entry_reg_channel, discord.TextChannel):
            raise ConfigError("Could not find entry registration channel")

        await entry_reg_channel.purge(limit=1)
        await entry_reg_channel.send(entry_reg_message, view=RegistrationBegin())


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        await member.send()

async def setup(bot: commands.Bot) -> None:
    with open(entry_reg_message_location, 'r') as file:
        global entry_reg_message
        entry_reg_message = file.read()
    with open(check_rules_message_location, 'r') as file:
        global check_rules_message
        check_rules_message = file.read()
    with open(wrong_word_message_location, 'r') as file:
        global wrong_word_message
        wrong_word_message = file.read()
    with open(pick_identities_message_location, 'r') as file:
        global pick_identities_message
        pick_identities_message = file.read()

    await bot.add_cog(Registration(bot))