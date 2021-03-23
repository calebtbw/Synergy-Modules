import discord
import asyncio
import contextlib
import copy
import time

from datetime import datetime
from typing import Optional, Union

from synergy.core import checks, commands, Config
from synergy.core.bot import Synergy
from synergy.core.utils.menus import menu, start_adding_reactions, DEFAULT_CONTROLS
from synergy.core.utils.mod import is_admin_or_superior
from synergy.core.utils.predicates import ReactionPredicate

__version__ = "1.0.2"
__author__ = "Caleb T."


class DaemonReports(commands.Cog):
    def __init__(self, bot: Synergy):
        self.bot: Synergy = bot

        default_guild = {
            # Initial Report Creation.
            "reaction": "🎫",
            "msg": "0-0",
            "openmessage": "{default}",
            # User Permissions Settings.
            "usercanclose": False,
            "usercanmodify": False,
            # Post-Creation Settings.
            "category": 0,
            "archive": {"category": 0, "enabled": False},
            "dm": False,
            # Misc
            "supportroles": [],
            "blacklist": [],
            "report": 0,
            "enabled": False,
            "created": {},
        }

        self.config = Config.get_conf(self, identifier=473541068378341376, force_registration=True)
        self.config.register_guild(**default_guild)
        self.config.register_global(first_migration=False)
        self.bot.loop.create_task(self.possibly_migrate())

    async def possibly_migrate(self):
        await self.bot.wait_until_synergy_ready()
        has_migrated = await self.config.first_migration()
        if not has_migrated:
            await self.migrate()

    async def migrate(self):
        guilds = self.config._get_base_group(self.config.GUILD)
        async with guilds.all() as data:
            for guild_id, guild_data in data.items():
                saving = {}
                try:
                    for user_id, report in guild_data["created"].items():
                        saving[user_id] = {"channel": report, "added": []}
                except KeyError:
                    continue

                data[guild_id]["created"] = saving
        await self.config.first_migration.set(True)

    async def embed_requested(self, channel):
        # Copy of ctx.embed_requested, but without context
        if not channel.permissions_for(channel.guild.me).embed_links:
            return False

        channel_setting = await self.bot._config.channel(channel).embeds()
        if channel_setting is not None:
            return channel_setting

        guild_setting = await self.bot._config.guild(channel.guild).embeds()
        if guild_setting is not None:
            return guild_setting

        return await self.bot._config.embeds()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        if not payload.guild_id:
            return

        guild_settings = await self.config.guild_from_id(payload.guild_id).all()
        if not guild_settings["enabled"]:
            return

        if guild_settings["msg"] == "0-0":
            await self.config.guild_from_id(payload.guild_id).enabled.set(False)
            return

        if guild_settings["msg"] != f"{payload.channel_id}-{payload.message_id}":
            return

        if (guild_settings["reaction"].isdigit() and payload.emoji.is_unicode_emoji()) or (
            not guild_settings["reaction"].isdigit() and payload.emoji.is_custom_emoji()
        ):
            return

        if payload.emoji.is_custom_emoji():
            if payload.emoji.id != int(guild_settings["reaction"]):
                return
        else:
            if str(payload.emoji) != guild_settings["reaction"]:
                return

        if str(payload.user_id) in guild_settings["created"]:
            # User already has a report.
            return

        category = self.bot.get_channel(guild_settings["category"])
        if not category:
            await self.config.guild_from_id(payload.guild_id).enabled.set(False)
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not category.permissions_for(guild.me).manage_channels:
            await self.config.guild_from_id(payload.guild_id).enabled.set(False)
            return

        if payload.user_id in guild_settings["blacklist"]:
            return

        user = guild.get_member(payload.user_id)
        admin_roles = [
            guild.get_role(role_id)
            for role_id in (await self.bot._config.guild(guild).admin_role())
            if guild.get_role(role_id)
        ]
        support_roles = [
            guild.get_role(role_id)
            for role_id in (await self.config.guild(guild).supportroles())
            if guild.get_role(role_id)
        ]

        all_roles = admin_roles + support_roles

        can_read = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        can_read_and_manage = discord.PermissionOverwrite(
            read_messages=True, send_messages=True, manage_channels=True, manage_permissions=True
        )  

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: can_read_and_manage,
            user: can_read,
        }
        for role in all_roles:
            overwrites[role] = can_read

        created_channel = await category.create_text_channel(
            f"report-{payload.user_id}", overwrites=overwrites
        )
        if guild_settings["openmessage"] == "{default}":
            if guild_settings["usercanclose"]:
                sent = await created_channel.send(
                    f"Report created for {user.display_name}\nTo close this, "
                    f"Staff or {user.display_name} may run `[p]daemonreports close`."
                )
            else:
                sent = await created_channel.send(
                    f"Report created for {user.display_name}\n"
                    "Only Staff may close this by running `[p]daemonreports close`."
                )
        else:
            try:
                message = (
                    guild_settings["openmessage"]
                    .replace("{mention}", user.mention)
                    .replace("{username}", user.display_name)
                    .replace("{id}", str(user.id))
                )
                sent = await created_channel.send(message)
            except Exception as e:
                # Something went wrong, let's go to default for now.
                print(e)
                if guild_settings["usercanclose"]:
                    sent = await created_channel.send(
                        f"Report created for {user.display_name}\nTo close this, "
                        f"Staff or {user.display_name} may run `[p]daemonreports close`."
                    )
                else:
                    sent = await created_channel.send(
                        f"Report created for {user.display_name}\n"
                        "Only Staff may close this by running `[p]daemonreports close`."
                    )
        
        embed = discord.Embed(title="Report Instructions",
                              description="Run `!dr create` and follow the instructions to create a report.", 
                                          color=discord.Color.blue())
        
        await created_channel.send(embed=embed)

        # To prevent race conditions.
        async with self.config.guild(guild).created() as created:
            created[payload.user_id] = {
                "channel": created_channel.id,
                "added": [],
                "opened": time.time(),
            }

        # If removing the reaction fails.
        with contextlib.suppress(discord.HTTPException):
            message = await self.bot.get_channel(payload.channel_id).fetch_message(
                payload.message_id
            )
            await message.remove_reaction(payload.emoji, member=user)

        if guild_settings["report"] != 0:
            reporting_channel = self.bot.get_channel(guild_settings["report"])
            if reporting_channel:
                if await self.embed_requested(reporting_channel):
                    embed = discord.Embed(
                        title="Daemon Report",
                        description=(
                            f"Report created by {user.mention} has been opened.\n"
                            f"Click [here]({sent.jump_url}) to jump to the start of the report."
                        ),
                        color=discord.Color.dark_green(), 
                        timestamp=datetime.utcnow()
                    )
                    description = ""
                    if guild_settings["usercanclose"]:
                        description += "Users are **allowed** to close their own reports.\n"
                    else:
                        description += "Users are **not** allowed to close their own reports.\n"

                    if guild_settings["usercanmodify"]:
                        description += (
                            "Users are **allowed** to add/remove "
                            "other users to/from their reports.\n"
                        )
                    else:
                        description += (
                            "Users are **not** allowed to add/remove "
                            "other users to/from their reports.\n"
                        )
                    embed.add_field(name="User Permission", value=description)
                    await reporting_channel.send(embed=embed)
                else:
                    message = (
                        f"Report created by {str(user)} has been opened.\n"
                        f"Here's a link ({sent.jump_url}) to jump to it.\n"
                    )

                    if guild_settings["usercanclose"] and guild_settings["usercanmodify"]:
                        message += (
                            "Users are **allowed** to close "
                            "and add/remove users to/from their reports."
                        )
                    elif guild_settings["usercanclose"]:
                        message += (
                            "Users are **allowed** to close their reports, "
                            "but cannot add/remove users."
                        )
                    elif guild_settings["usercanmodify"]:
                        message += (
                            "Users are **allowed** to add/remove users to/from their reports, "
                            "but are **not** allowed to close it."
                        )
                    else:
                        message += "Users cannot close or add/remove users to/from their reports."

                    await reporting_channel.send(message)

    @checks.bot_has_permissions(add_reactions=True)
    @commands.guild_only()
    @commands.group(aliases=["dr"])
    async def daemonreports(self, ctx):
        """Create a reaction report system in GGServers Discord."""
        pass

    @daemonreports.command()
    async def help(self, ctx):
        """Daemon Reports system commands."""
        embed = discord.Embed(title="Daemon Reports System Commands:",
                              description="**!dr add** - Adds a user to the current daemon report.\n"
                                          "**!dr close** - Close the created report.\n"
                                          "**!dr create** - For users to input their Node ID and Error.\n"
                                          "**!dr remove** - Remove a user from the current report.\n"
                                          "**!dr settings** - Manage settings for daemon reports.", 
                                          color=discord.Color.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @daemonreports.command()
    async def create(self, ctx):
        """For users to input their Node ID and Error.
        To be used in the created channel only."""
        initial_msg = await ctx.send(
            "You will be asked 2 questions for information regarding your daemon report. Please respond accordingly."
        )

        def check(message):
            return message.author.id == ctx.message.author.id and message.content != ""

        q1 = await ctx.send(
            "Please input your Node ID:"
        )
        try:
            r1 = await self.bot.wait_for(
                "message", timeout=60, check=check
            )
            node = r1.content

        except asyncio.TimeoutError:
            await ctx.send(
                "You took too long to provide the requested information.\n"
                "Please try again by running `!dr create`."
            )
            return
      
        q2 = await ctx.send(
            "Please state the Error Message:"
        )
        try:
            r2 = await self.bot.wait_for(
                "message", timeout=60, check=check
            )
            error = r2.content

        except asyncio.TimeoutError:
            await ctx.send(
                "You took too long to provide the requested information.\n"
                "Please try again by running `!dr create`."
            )
            return       
    
        e = discord.Embed(
            title="Daemon Report Info",
            description="For Staff to note the reported Node ID and Error Message.",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )

        fields = [
            ("Node ID:", f"{node}", False),
            ("Error:", f"{error}", False)
        ]

        for name, value, inline in fields:
            e.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=e)
        return await ctx.send(
            "Thank you for reporting the issue. Any updates to the report will be done so via this channel."
        )

    @daemonreports.command()
    async def close(self, ctx, *, reason=None):
        """Close the created report.
        If run by a normal user, this will default to the user.
        If run by a member of staff or support, this will check the channel."""
        guild_settings = await self.config.guild(ctx.guild).all()
        is_admin = await is_admin_or_superior(self.bot, ctx.author) or any(
            [ur.id in guild_settings["supportroles"] for ur in ctx.author.roles]
        )
        must_be_admin = not guild_settings["usercanclose"]

        if not is_admin and must_be_admin:
            await ctx.send("Only Staff can close reports.")
            return
        elif not is_admin:
            author = ctx.author
            author_id = author.id
        elif is_admin:
            # Try to get the current channel and get the author.
            # If not, we'll default to ctx.author.
            inverted = {}
            for author_id, report in guild_settings["created"].items():
                inverted[report["channel"]] = author_id
            try:
                author = ctx.guild.get_member(int(inverted[ctx.channel.id]))
                if author:
                    author_id = author.id
                else:
                    author_id = int(inverted[ctx.channel.id])
            except KeyError:
                author = ctx.author
                author_id = author.id

        if str(author_id) not in guild_settings["created"]:
            await ctx.send("That user does not have an open report.")
            return

        channel = self.bot.get_channel(guild_settings["created"][str(author_id)]["channel"])
        archive = self.bot.get_channel(guild_settings["archive"]["category"])
        added_users = [
            user
            for u in guild_settings["created"][str(author_id)]["added"]
            if (user := ctx.guild.get_member(u))
        ]
        added_users.append(author)

        if ctx.message.channel != channel:
            await ctx.send("Please run the command in the corresponding channel.")
            return
        else:
            message = await ctx.send(
                "Are you sure you want to close this report?\n"
                "Note: This action is irreversible."
            )

        start_adding_reactions(message, ReactionPredicate.YES_OR_NO_EMOJIS)
        pred = ReactionPredicate.yes_or_no(message, ctx.author)
        await self.bot.wait_for("reaction_add", check=pred)
        if pred.result is True:
            await message.delete()    
            # Again, to prevent race conditions.
            async with self.config.guild(ctx.guild).created() as created:
                del created[str(author_id)]

            if guild_settings["report"] != 0:
                reporting_channel = self.bot.get_channel(guild_settings["report"])
                if reporting_channel:
                    if await self.embed_requested(reporting_channel):
                        embed = discord.Embed(
                            title="Report Closed",
                            description=(
                                f"Report created by {author.mention if author else author_id} "
                                f"has been closed by {ctx.author.mention}."
                            ),
                            color=discord.Color.dark_red(), 
                            timestamp=datetime.utcnow()
                        )
                        if reason:
                            embed.add_field(name="Reason", value=reason)
                        await reporting_channel.send(embed=embed)
                    else:
                        message = (
                            f"Report created by {str(author) if author else author_id} "
                            f"has been closed by {str(ctx.author)}."
                        )
                        if reason:
                            message += f"\n**Reason**: {reason}"

                        await reporting_channel.send(message)

            if guild_settings["dm"] and author:
                embed = discord.Embed(
                    title="Report Closed",
                    description=(f"Your report has been closed by {ctx.author.mention}."),
                    color=discord.Color.dark_red(), 
                    timestamp=datetime.utcnow()
                )
                if reason:
                    embed.add_field(name="Reason", value=reason)
                with contextlib.suppress(discord.HTTPException):
                    await author.send(embed=embed)

            if guild_settings["archive"]["enabled"] and channel and archive:
                for user in added_users:
                    with contextlib.suppress(discord.HTTPException):
                        if user:
                            await channel.set_permissions(
                                user, send_messages=False, read_messages=True
                            )
                await ctx.send(
                    f"Report for {author.display_name if author else author_id} has been closed.\n"
                    "Channel will be moved to archive in 10 seconds."
                )

                await asyncio.sleep(10)

                try:
                    admin_roles = [
                        ctx.guild.get_role(role_id)
                        for role_id in (await self.bot._config.guild(ctx.guild).admin_role())
                        if ctx.guild.get_role(role_id)
                    ]
                    support_roles = [
                        ctx.guild.get_role(role_id)
                        for role_id in (await self.config.guild(ctx.guild).supportroles())
                        if ctx.guild.get_role(role_id)
                    ]

                    all_roles = admin_roles + support_roles
                    overwrites = {
                        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        ctx.guild.me: discord.PermissionOverwrite(
                            read_messages=True,
                            send_messages=True,
                            manage_channels=True,
                            manage_permissions=True,
                        ),
                    }
                    for role in all_roles:
                        overwrites[role] = discord.PermissionOverwrite(
                            read_messages=True, send_messages=True
                        )
                    for user in added_users:
                        if user:
                            overwrites[user] = discord.PermissionOverwrite(read_messages=False)
                    await channel.edit(category=archive, overwrites=overwrites)
                except discord.HTTPException as e:
                    await ctx.send(f"Failed to move to archive: {str(e)}")
            else:
                if channel:
                    for user in added_users:
                        with contextlib.suppress(discord.HTTPException):
                            if user:
                                await channel.set_permissions(
                                    user, send_messages=False, read_messages=True
                                )
                await ctx.send(
                    f"Report for {author.display_name if author else author_id} has been closed.  "
                    "Channel will be deleted in 10 seconds, if it exists."
                )

                await asyncio.sleep(10)

                if channel:
                    try:
                        await channel.delete()
                    except discord.HTTPException:
                        with contextlib.suppress(discord.HTTPException):
                            await ctx.send(
                                "Failed to delete channel. Please ensure I have `Manage Channels` "
                                "permission in the category."
                            )
        else:
            await ctx.send("Report closure cancelled.")
            return await message.delete()

    @daemonreports.command(name="add")
    async def report_add(self, ctx, user: discord.Member):
        """Adds a user to the current daemon report."""
        guild_settings = await self.config.guild(ctx.guild).all()
        is_admin = await is_admin_or_superior(self.bot, ctx.author) or any(
            [ur.id in guild_settings["supportroles"] for ur in ctx.author.roles]
        )
        must_be_admin = not guild_settings["usercanmodify"]

        if not is_admin and must_be_admin:
            await ctx.send("Only Staff can add/remove other users to reports.")
            return
        elif not is_admin:
            author = ctx.author
            author_id = author.id
        elif is_admin:
            # Since the author isn't specified, and it's an admin, we need to guess on who
            # the author is
            inverted = {}
            for author_id, report in guild_settings["created"].items():
                inverted[report["channel"]] = author_id
            try:
                author = ctx.guild.get_member(int(inverted[ctx.channel.id]))
                if author:
                    author_id = author.id
                else:
                    author_id = int(inverted[ctx.channel.id])
            except KeyError:
                author = ctx.author
                author_id = author.id

        if str(author_id) not in guild_settings["created"]:
            if not is_admin:
                await ctx.send("You do not have an open report.")
            else:
                await ctx.send(
                    "Failed to determine report.\n"
                    "Please run command in the corresponding report channel."
                )
            return

        if user.id in guild_settings["created"][str(author_id)]["added"]:
            await ctx.send("That user is already added.")
            return

        adding_is_admin = await is_admin_or_superior(self.bot, user) or any(
            [ur.id in guild_settings["supportroles"] for ur in user.roles]
        )

        if adding_is_admin:
            await ctx.send("Members of Staff cannot be added to reports.")
            return

        channel = self.bot.get_channel(guild_settings["created"][str(author_id)]["channel"])
        if not channel:
            await ctx.send("The report channel has been deleted.")

        try:
            await channel.set_permissions(user, send_messages=True, read_messages=True)
        except discord.Forbidden:
            await ctx.send(
                "The manage permissions channel permission for me has been removed. "
                "I am unable to modify this report."
            )
            return

        async with self.config.guild(ctx.guild).created() as created:
            created[str(author_id)]["added"].append(user.id)

        await ctx.send(f"{user.mention} has been added to the report.")

    @daemonreports.command(name="remove")
    async def report_remove(self, ctx, user: discord.Member):
        """Remove a user from the current report."""
        guild_settings = await self.config.guild(ctx.guild).all()
        is_admin = await is_admin_or_superior(self.bot, ctx.author) or any(
            [ur.id in guild_settings["supportroles"] for ur in ctx.author.roles]
        )
        must_be_admin = not guild_settings["usercanmodify"]

        if not is_admin and must_be_admin:
            await ctx.send("Only Staff can add/remove other users to reports.")
            return
        elif not is_admin:
            author = ctx.author
            author_id = author.id
        elif is_admin:
            # Since the author isn't specified, and it's an admin, we need to guess on who
            # the author is
            inverted = {}
            for author_id, report in guild_settings["created"].items():
                inverted[report["channel"]] = author_id
            try:
                author = ctx.guild.get_member(int(inverted[ctx.channel.id]))
                if author:
                    author_id = author.id
                else:
                    author_id = int(inverted[ctx.channel.id])
            except KeyError:
                author = ctx.author
                author_id = author.id

        if str(author_id) not in guild_settings["created"]:
            if not is_admin:
                await ctx.send("You do not have an open report.")
            else:
                await ctx.send(
                    "Failed to determine report. "
                    "Please run command in the corresponding report channel."
                )
            return

        if user.id not in guild_settings["created"][str(author_id)]["added"]:
            await ctx.send("That user is not added.")
            return

        removing_is_admin = await is_admin_or_superior(self.bot, user) or any(
            [ur.id in guild_settings["supportroles"] for ur in user.roles]
        )

        if removing_is_admin:
            await ctx.send("Members of Staff cannot be removed from reports.")
            return

        channel = self.bot.get_channel(guild_settings["created"][str(author_id)]["channel"])
        if not channel:
            await ctx.send("The report channel has been deleted.")

        try:
            await channel.set_permissions(user, send_messages=False, read_messages=False)
        except discord.Forbidden:
            await ctx.send(
                "The manage permissions channel permission for me has been removed. "
                "I am unable to modify this report."
            )
            return

        async with self.config.guild(ctx.guild).created() as created:
            created[str(author_id)]["added"].remove(user.id)

        await ctx.send(f"{user.mention} has been removed from the report.")

    @checks.admin_or_permissions(manage_guild=True)
    @daemonreports.group(invoke_without_command=True)
    async def settings(self, ctx):
        """Manage settings for daemon reports."""
        drs1 = discord.Embed(title="Daemon Reports Settings Commands:",
                             description="**!dr settings archive** - Customize settings for archiving daemon report channels.\n"
                                         "**!dr settings blacklist** - Add or remove a user to be prevented from creating reports.\n"
                                         "**!dr settings category** - Set the category to create new daemon report channels under.\n"
                                         "**!dr settings creationmessage** - Set the message that is sent when users create a report.\n"
                                         "**!dr settings disable** - Disable reporting system.\n"
                                         "**!dr settings dm** - Set whether or not to send a DM to the report author once a report is closed.\n"
                                         "**!dr settings enable** - Enable reporting system.", 
                                         color=discord.Color.blue())

        drs1.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        drs1.set_footer(text="Note: There are subcommands for some of these. | Page 1 of 2")

        drs2 = discord.Embed(title="Daemon Reports Settings Commands:",
                             description="**!dr settings purge** - Clean out channels under the archive category.\n"
                                         "**!dr settings reaction** - Set the reaction to listen for on the report creation message.\n"
                                         "**!dr settings reports** - Set a channel that logs when a report is opened or closed.\n"
                                         "**!dr settings roles** - Add or remove a role to be automatically added to new reports.\n"
                                         "**!dr settings setmsg** - Set the message to listen for report reactions on.\n"
                                         "**!dr settings usercanclose** - Set whether users can close their own reports.\n"
                                         "**!dr settings usercanmodify** - Set whether users can add/remove users from their own reports.", 
                                         color=discord.Color.blue())

        drs2.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        drs2.set_footer(text="Note: There are subcommands for some of these. | Page 2 of 2")

        guild_settings = await self.config.guild(ctx.guild).all()
        channel_id, message_id = list(map(int, guild_settings["msg"].split("-")))

        report_channel = getattr(self.bot.get_channel(channel_id), "name", "Not set")
        report_category = getattr(
            self.bot.get_channel(guild_settings["category"]), "name", "Not set"
        )
        archive_category = getattr(
            self.bot.get_channel(guild_settings["archive"]["category"]), "name", "Not set"
        )
        report_channel = getattr(self.bot.get_channel(guild_settings["report"]), "name", "Not set")

        pages = [drs1, drs2]

        await ctx.send(
            "```ini\n"
            f"[Report Channel]:    {report_channel}\n"
            f"[Report MessageID]:  {message_id}\n"
            f"[Report Reaction]:   {guild_settings['reaction']}\n"
            f"[User-Closable]:     {guild_settings['usercanclose']}\n"
            f"[User-Modifiable]:   {guild_settings['usercanmodify']}\n"
            f"[Report Category]:   {report_category}\n"
            f"[Report Channel]:    {report_channel}\n"
            f"[Report Close DM]:   {guild_settings['dm']}\n"
            f"[Archive Category]:  {archive_category}\n"
            f"[Archive Enabled]:   {guild_settings['archive']['enabled']}\n"
            f"[System Enabled]:    {guild_settings['enabled']}\n"
            "```"
        )

        await menu(ctx, pages, DEFAULT_CONTROLS)

    @settings.command()
    async def setmsg(self, ctx, message: discord.Message):
        """Set the message to listen for report reactions on."""
        if not message.channel.permissions_for(ctx.guild.me).manage_messages:
            await ctx.send(
                'I require the "Manage Messages" permission in that channel to execute that command.'
            )
            return

        msg = f"{message.channel.id}-{message.id}"
        await self.config.guild(ctx.guild).msg.set(msg)
        await ctx.send("Report message successfully set.")

    @settings.command()
    async def reaction(self, ctx, emoji: Union[discord.Emoji, str]):
        """Set the reaction to listen for on the Daemon Report creation message."""
        if isinstance(emoji, discord.Emoji):
            if emoji.guild_id != ctx.guild.id:
                await ctx.send(
                    "Custom emojis must be from the same guild the Daemon Reports system "
                    "is being set up in."
                )
                return
            test_emoji = emoji
            emoji = str(emoji.id)
        else:
            emoji = str(emoji).replace("\N{VARIATION SELECTOR-16}", "")
            test_emoji = emoji

        test_message = None
        channel_id, message_id = list(
            map(int, (await self.config.guild(ctx.guild).msg()).split("-"))
        )

        if channel_id == message_id == 0:
            test_message = ctx.message
        else:
            try:
                test_message = await self.bot.get_channel(channel_id).fetch_message(message_id)
            except (AttributeError, discord.NotFound, discord.Forbidden):
                # Channel/message no longer exists or we cannot access it.
                await self.config.guild(ctx.guild).msg.set("0-0")
                test_message = ctx.message

        try:
            await test_message.add_reaction(test_emoji)
        except discord.HTTPException:
            await ctx.send("Invalid emoji.")
            return
        else:
            await test_message.remove_reaction(test_emoji, member=ctx.guild.me)

        await self.config.guild(ctx.guild).reaction.set(emoji)
        await ctx.send(f"Report reaction successfully set to {test_emoji}")

    @settings.command(name="creationmessage", aliases=["openmessage"])
    async def report_creation_message(self, ctx, *, message):
        """Set the message that is sent when you initially create the report.

        If any of these are included in the message, they will automatically be
        replaced with the corresponding value.

        {mention} - Mentions the user who created the report
        {username} - Username of the user who created the report
        {id} - ID of the user who created the report.

        To return to default, set the message to exactly "{default}" """
        await self.config.guild(ctx.guild).openmessage.set(message)
        if message == "{default}":
            await ctx.send("Report creation message restored to default.")
        else:
            await ctx.send("Report creation message successfully set.")

    @settings.command()
    async def usercanclose(self, ctx, yes_or_no: Optional[bool] = None):
        """Set whether users can close their own daemon reports or not."""
        if yes_or_no is None:
            yes_or_no = not await self.config.guild(ctx.guild).usercanclose()

        await self.config.guild(ctx.guild).usercanclose.set(yes_or_no)
        if yes_or_no:
            await ctx.send("Users can now close their own reports.")
        else:
            await ctx.send("Only Staff can now close reports.")

    @settings.command()
    async def usercanmodify(self, ctx, yes_or_no: Optional[bool] = None):
        """Set whether users can add or remove additional users to their daemon report."""
        if yes_or_no is None:
            yes_or_no = not await self.config.guild(ctx.guild).usercanmodify()

        await self.config.guild(ctx.guild).usercanmodify.set(yes_or_no)
        if yes_or_no:
            await ctx.send("Users can now add/remove other users to their own reports.")
        else:
            await ctx.send("Only Staff can now add/remove users to reports.")

    @settings.command()
    async def blacklist(self, ctx, *, user: discord.Member = None):
        """Add or remove a user to be prevented from creating daemon reports.
        Useful for users who are creating reports for no reason."""
        if user:
            async with self.config.guild(ctx.guild).blacklist() as blacklist:
                if user.id in blacklist:
                    blacklist.remove(user.id)
                    await ctx.send(
                        f"{user.display_name} has been removed from the Daemon Reports blacklist."
                    )
                else:
                    blacklist.append(user.id)
                    await ctx.send(
                        f"{user.display_name} has been added to the Daemon Reports blacklist."
                    )
        else:
            blacklist = await self.config.guild(ctx.guild).blacklist()
            if not blacklist:
                await ctx.send("No users have been blacklisted so far.")
                return
            e = discord.Embed(
                title="The following users are blacklisted from creating reports.",
                description="",
                color=await ctx.embed_color(), 
                timestamp=datetime.utcnow()
            )
            for u in blacklist:
                e.description += f"<@{u}> "
            await ctx.send(embed=e)

    @settings.command()
    async def roles(self, ctx, *, role: discord.Role = None):
        """Add or remove a role to be automatically added to daemon report channels.
        These will be seen as support roles, and will have access to archived daemon report channels."""
        if role:
            async with self.config.guild(ctx.guild).supportroles() as roles:
                if role.id in roles:
                    roles.remove(role.id)
                    await ctx.send(
                        f"The {role.name} role will no longer be automatically added to reports."
                    )
                else:
                    roles.append(role.id)
                    await ctx.send(
                        f"The {role.name} role will now automatically be added to reports."
                    )
        else:
            roles = await self.config.guild(ctx.guild).supportroles()
            new = copy.deepcopy(roles)
            if not roles:
                await ctx.send("No roles are set to be added to reports right now.")
                return
            e = discord.Embed(
                title="The following roles are automatically added to reports.",
                description="Note that staff roles will always be added by default.\n",
                color=await ctx.embed_color(), 
                timestamp=datetime.utcnow() 
            )
            for r in roles:
                ro = ctx.guild.get_role(r)
                if ro:
                    e.description += ro.mention + "\n"
                else:
                    new.remove(r)

            if new != roles:
                await self.config.guild(ctx.guild).supportroles.set(new)
            await ctx.send(embed=e)

    @settings.command()
    async def category(self, ctx, category: discord.CategoryChannel):
        """Set the category to create daemon report channels under."""
        if not category.permissions_for(ctx.guild.me).manage_channels:
            await ctx.send(
                'I require the "Manage Channels" permission in that category to execute that command.'
            )
            return

        await self.config.guild(ctx.guild).category.set(category.id)
        await ctx.send(f"Report channels will now be created in the {category.name} category")

    @settings.group()
    async def archive(self, ctx):
        """Customize settings for archiving daemon report channels."""
        pass

    @archive.command(name="category")
    async def archive_category(self, ctx, category: discord.CategoryChannel):
        """Set the category to move closed report channels to."""
        if not category.permissions_for(ctx.guild.me).manage_channels:
            await ctx.send(
                'I require the "Manage Channels" permission in that category to execute that command.'
            )
            return

        async with self.config.guild(ctx.guild).archive() as data:
            data["category"] = category.id
        await ctx.send(
            f"Closed report channels will now be moved to the {category.name} category, "
            "if Archive mode is enabled."
        )

    @archive.command(name="enable")
    async def archive_enable(self, ctx, yes_or_no: bool = None):
        """Enable Archiving mode, to move the Report Channels to the set category once closed."""
        async with self.config.guild(ctx.guild).archive() as data:
            if yes_or_no is None:
                data["enabled"] = not data["enabled"]
                yes_or_no = data["enabled"]
            else:
                data["enabled"] = yes_or_no

        if yes_or_no:
            await ctx.send("Archiving mode is now enabled.")
        else:
            await ctx.send("Archiving mode is now disabled.")

    @settings.command()
    async def reports(self, ctx, channel: discord.TextChannel = None):
        """Set a channel that logs when a report is opened or closed.
        If left blank, this will disable reports."""
        saving = getattr(channel, "id", 0)
        await self.config.guild(ctx.guild).report.set(saving)

        if not channel:
            await ctx.send("Daemon Reports logging has been disabled.")
        else:
            await ctx.send(f"Daemon Reports logging has been set to {channel.mention}")

    @settings.command()
    async def dm(self, ctx, yes_or_no: bool = None):
        """Set whether or not to send a DM to the report author on daemon report close."""
        if yes_or_no is None:
            yes_or_no = not await self.config.guild(ctx.guild).dm()

        await self.config.guild(ctx.guild).dm.set(yes_or_no)
        if yes_or_no:
            await ctx.send("Users will now be DMed a message when their report is closed.")
        else:
            await ctx.send("Users will no longer be DMed a message when their report is closed.")

    @settings.command(name="prune", aliases=["purge"])
    async def report_channel_prune(self, ctx, user: Optional[Union[int, discord.User]] = None):
        """Clean out channels under the archive category.
        Pass a user to only delete the channels created by that user instead.
        WARNING: This will remove ALL channels unless otherwise specified!"""
        category = self.bot.get_channel((await self.config.guild(ctx.guild).archive())["category"])
        if not category:
            await ctx.send("Channels related to that category cannot be found or have been purged!")
            return

        if isinstance(user, discord.User):
            user = user.id

        channels = []
        if user:
            for channel in category.text_channels:
                if channel.name == f"report-{user}":
                    channels.append(channel)
            message = await ctx.send(
                f"Are you sure you want to remove all archived report channels from user {user}?\n"
                f"This will delete {len(channels)} Text Channels."
            )
        else:
            channels = category.text_channels
            message = await ctx.send(
                "Are you sure you want to remove all archived report channels?\n"
                f"This will delete {len(channels)} Text Channels."
            )

        start_adding_reactions(message, ReactionPredicate.YES_OR_NO_EMOJIS)
        pred = ReactionPredicate.yes_or_no(message, ctx.author)
        await self.bot.wait_for("reaction_add", check=pred)
        if pred.result is True:
            await message.delete()
            progress = await ctx.send("Purging text channels...")
            for channel in channels:
                try:
                    await channel.delete()
                except discord.Forbidden:
                    await ctx.send(
                        "I do not have permission to delete those text channels.\n"
                        'Make sure I have "Manage Channels" permission.'
                    )
                    return
                except discord.HTTPException:
                    continue

            await progress.edit(content="Channels successfully purged.")
        else:
            await ctx.send("Channel purge cancelled.")
            return await message.delete()

    @settings.command()
    async def enable(self, ctx):
        """Starts listening for the set Reaction on the set Message to process daemon reports."""
        # We'll run through a test of all the settings to ensure everything is set properly.
        message = await ctx.send(
            "Enable Daemon Reports system?\n"
            "Checks will be done before fully enabling it."
        )
        start_adding_reactions(message, ReactionPredicate.YES_OR_NO_EMOJIS)
        pred = ReactionPredicate.yes_or_no(message, ctx.author)
        await self.bot.wait_for("reaction_add", check=pred)
        if pred.result is True:
            await message.delete()
            progress = await ctx.send("Running checks...")

            # 1 - Report message is accessible and we can do what is needed with it
            channel_id, message_id = list(
                map(int, (await self.config.guild(ctx.guild).msg()).split("-"))
            )
            if channel_id == message_id == 0:
                await ctx.send(
                    "Please set the message to listen on first with "
                    f"`{ctx.prefix}daemonreports settings setmsg`."
                )
                return

            try:
                message = await self.bot.get_channel(channel_id).fetch_message(message_id)
            except AttributeError:
                # Channel no longer exists.
                await self.config.guild(ctx.guild).msg.set("0-0")
                await ctx.send(
                    f"Please reset the message to listen on `{ctx.prefix}daemonreports settings setmsg`."
                    "\nReason: Channel has been deleted"
                )
                return
            except discord.NotFound:
                # Message no longer exists.
                await self.config.guild(ctx.guild).msg.set("0-0")
                await ctx.send(
                    f"Please reset the message to listen on `{ctx.prefix}daemonreports settings setmsg`."
                    "\nReason: Message has been deleted"
                )
                return

            # 2 - Check reaction is set properly
            emoji = await self.config.guild(ctx.guild).reaction()
            if emoji.isdigit():
                emoji = self.bot.get_emoji(int(emoji))
                if not emoji:
                    await self.config.guild(ctx.guild).reaction.set("🎫")
                    await ctx.send(
                        "Set custom emoji is invalid. Please ensure that the emoji still exists.\n"
                        "If you would like to bypass this and go with the default, "
                        "re-run this command."
                    )
                    return

            try:
                await message.add_reaction(emoji)
            except discord.HTTPException:
                await ctx.send(
                    "Failed to react to set message with emoji.\n"
                    "Are you sure the emoji is valid and I have the Add Reactions permission?"
                )
                return

            # 3 - Category check
            category_id = await self.config.guild(ctx.guild).category()
            if not category_id:
                await ctx.send(
                    "Please set the category to create report channels under with "
                    f"`{ctx.prefix}daemonreports settings category`."
                )
                return

            category = self.bot.get_channel(category_id)
            if not category:
                await ctx.send(
                    "Please reset the category to create report channels under with "
                    f"`{ctx.prefix}daemonreports settings category`.\n"
                    "Reason: Category has been deleted."
                )
                return

            # 4 - Archive check (if enabled)
            archive = await self.config.guild(ctx.guild).archive()
            if archive["enabled"]:
                if not archive["category"]:
                    await ctx.send(
                        "Archive mode is enabled but no category is set.\n"
                        f"Please set one with `{ctx.prefix}daemonreports settings archive category`."
                    )
                    return

                archive_category = self.bot.get_channel(archive["category"])
                if not archive_category:
                    await ctx.send(
                        "Archive mode is enabled but set category does not exist.\n"
                        f"Please reset it with `{ctx.prefix}daemonreports settings archive category`."
                    )
                    return

                if not archive_category.permissions_for(ctx.guild.me).manage_channels:
                    await ctx.send(
                        "Archive mode is enabled but I do not have permission to manage channels in "
                        "set category. Please reconfigure my permissions to allow me to "
                        '"Manage Channels".'
                    )
                    return

            # 5 - Reporting channel (also if enabled)
            report = await self.config.guild(ctx.guild).report()
            if report != 0:
                report_channel = self.bot.get_channel(report)
                if not report_channel:
                    await ctx.send(
                        "Reporting is enabled but the channel has been deleted.\n"
                        f"Please reset it with `{ctx.prefix}daemonreports settings report`."
                    )

                if not report_channel.permissions_for(ctx.guild.me).send_messages:
                    await ctx.send(
                        "Reporting is enabled but I do not have proper permissions.\n"
                        "Please reconfigure my permissions to allow me to Read and Send Messages."
                    )
                    return

            # Checks passed, let's cleanup a little bit and then enable it.
            await message.clear_reactions()
            await message.add_reaction(emoji)
            await self.config.guild(ctx.guild).enabled.set(True)

            await progress.edit(content="Checks complete. Daemon Reports system is now active.")

        else:
            await message.delete()
            return await ctx.send("Daemon Reports system will not be enabled.")

    @settings.command()
    async def disable(self, ctx):
        """Disable reporting system"""
        message = message = await ctx.send(
            "Disable Daemon Reports system?\n"
        )
        start_adding_reactions(message, ReactionPredicate.YES_OR_NO_EMOJIS)
        pred = ReactionPredicate.yes_or_no(message, ctx.author)
        await self.bot.wait_for("reaction_add", check=pred)
        if pred.result is True:
            await message.delete()
            await self.config.guild(ctx.guild).enabled.set(False)
            await ctx.send("Daemon Reports system disabled.")
        else:
            await message.delete()
            return await ctx.send("Daemon Reports system will not be disabled.")
