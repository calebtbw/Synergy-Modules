import discord
import asyncio

from synergy.core import commands, checks, Config
from synergy.core.utils.menus import menu, DEFAULT_CONTROLS

from discord.ext.commands import has_permissions, MissingPermissions


class HelpDesk(commands.Cog):
    """
        Commands to send out Helpdesk articles.
    """
    def __init__(self, bot):
        self.bot = bot

    __author__ = ["Middel#9816", "Caleb T.#0945"]
    __version__ = "1.6.6"

    def whitelist(ctx):
        return ctx.message.guild.id in [808533625016156220]

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def helpdesk(self, ctx):
        """
            GGServers Helpdesk Commands.
        """
        hd1 = discord.Embed(title="Discord Helpdesk Commands:",
                            description="**!offline** - Minecraft offline mode.\n"
                                        "**!pending** - Service is pending.\n"
                                        "**!op** - OP yourself on your Minecraft server.\n"
                                        "**!ticket** - Support ticket instructions.\n"
                                        "**!accounts** - Give Multicraft access to a friend. (sub account)\n"
                                        "**!datapacks** - Installing datapacks on your server.\n"
                                        "**!whatpremium** - Differences between premium and standard plans.\n"
                                        "**!plans** - Shows all our plans.\n"
                                        "**!luckperms** - Displays all relevant Luckperms information.\n"
                                        "**!allbackup** - Shows all information needed for backups.\n"
                                        "**!allftp** - Shows Filezilla, WinSCP & Multicraft ftp usage and information.\n"
                                        "**!allupgrade** - Shows information about upgrades.\n"
                                        "**!multialts** - Shows Multicraft alternate links.\n"
                                        "**!refund** - Shows our refund policy information.\n"
                                        "**!native** - Shows memory error information.\n"
                                        "**!modsplugins** - Shows anything mods & plugins related.\n"
                                        "**!performance** - Shows all performance related guides.\n"
                                        "**!resetpass** - Shows all password related guides.\n"
                                        "**!custom** - Shows custom installation guides.\n"
                                        "**!allworld** - Shows all world related guides.\n"
                                        "**!worldmgmt** - Shows all world management guides.\n"
                                        "**!fabric** - Shows fabric guide.\n"
                                        "**!daemon** - Daemon issues related information.", color=discord.Colour.blue())

        hd1.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        hd1.set_footer(text="Made by: Fabian & Caleb | Helpdesk v1.6.6 | Page 1 of 3")

        hd2 = discord.Embed(title="Discord Helpdesk Commands:",
                            description="**!cmds** - Vanilla/Custom commands.\n"
                                        "**!biomesop** - Biomes O. Plenty mod information.\n"
                                        "**!tebex** - TEBEX - Buycraft setup information.\n"
                                        "**!plugins** - Plugin installation information.\n"
                                        "**!cc3** - Crazycraft 3.0 not working?\n"
                                        "**!scramble** - Turn scrambled recipes off.\n"
                                        "**!ticketbedrock** - Ticket for Bedrock node movement.\n"
                                        "**!bedrock** - Bedrock related information.\n"
                                        "**!logs** - Shows how to send server logs.\n"
                                        "**!multidown** - Multicraft is down information.\n"
                                        "**!clearcache** - Error 524 information.\n"
                                        "**!eta** - ETA on tickets.\n" 
                                        "**!customdomain** - Custom domain URLs.\n"
                                        "**!clean** - Clean installation.\n"
                                        "**!fly** - Flying not enabled.\n"
                                        "**!mods** - Mods installation.\n"
                                        "**!watchdog** - Disables watchdog.\n"
                                        "**!whitelisting** - Whitelist setup.\n"
                                        "**!credentials** - Multicraft credentials.\n"
                                        "**!ticking** - Ticking entity.\n"
                                        "**!entitypurge** - Entity purge tool.\n"
                                        "**!jsonvalidator** - JSON Validator usage.\n"
                                        "**!openport** - Finding an open port.", color=discord.Colour.blue())

        hd2.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        hd2.set_footer(text="Made by: Fabian & Caleb | Helpdesk v1.6.6 | Page 2 of 3")

        hd3 = discord.Embed(title="Discord Helpdesk Commands:",
                            description="**!cancel** - Cancel your service.", color=discord.Colour.blue())

        hd3.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        hd3.set_footer(text="Made by: Fabian & Caleb | Helpdesk v1.6.6 | Page 3 of 3")
        """Essentially if there are more pages in the future, we can simply have hd3, hd4 etc...
        Let's keep the len at 23 per page."""
        pages = [hd1, hd2, hd3] 

        await menu(ctx, pages, DEFAULT_CONTROLS)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def offline(self, ctx):
        """
            Minecraft offline mode command.
        """
        embed = discord.Embed(title="Minecraft offline mode!",
                              description="[How to: Change your server to offline mode!](https://help.ggservers.com/en-us/article/how-to-change-your-server-to-offline-mode-1l5bcz6/)", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def pending(self, ctx):
        """
            Pending service command.
        """
        embed = discord.Embed(title="Pending Service",
                              description="If your server is pending that means that we are still setting up your new server. Most of the time, it happens instantly. In other instances though, we have to do some setup.", color=discord.Colour.blue())

        fields = [("Why is my service pending?", "[Knowledgebase](https://help.ggservers.com/en-us/article/pending-service-5sdugh/)", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def op(self, ctx):
        """
            How to OP yourself command.
        """
        embed = discord.Embed(title="How to: OP Yourself on your minecraft server!",
                              description="[How to: OP yourself on your Minecraft server!](https://help.ggservers.com/en-us/article/how-to-op-yourself-on-your-minecraft-server-1l4zakc/)", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)
  
    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def ticket(self, ctx):
        """
            How to open a support ticket command.
        """
        embed = discord.Embed(title="Support ticket instructions!",
                              description="[How to: open a support ticket with us!](https://help.ggservers.com/en-us/article/how-to-open-a-support-ticket-qjzuyd/)", color=discord.Colour.blue())
        
        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def accounts(self, ctx):
        """
            How to give Multicraft access to a friend (sub accounts)
        """
        embed = discord.Embed(title="Multicraft Sub accounts guide!",
                              description="[How to: Give Multicraft access to a friend (sub accounts)!](https://help.ggservers.com/en-us/article/how-to-give-multicraft-access-to-a-friend-sub-account-16u5tri/)", color=discord.Colour.blue())
        
        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def datapacks(self, ctx):
        """
            Installing datapacks on your server
        """
        embed = discord.Embed(title="Minecraft Datapacks!",
                              description="[How to: Install datapacks on your server!](https://help.ggservers.com/en-us/article/how-to-install-datapacks-on-your-server-nmp6zs/)", color=discord.Colour.blue())
        
        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def whatpremium(self, ctx):
        """
            Differences between premium and standard plans.
        """
        premium = discord.Embed(title="-- Premium --", description="[Knowledgebase](https://help.ggservers.com/en-us/article/the-difference-between-standard-premium-104nqdh/)", 
                       color=discord.Colour.blue())

        fields = [("Price/mo:", "$6/GB", False),
                  ("Locations:", "Canada | UK | France | Germany | Finland | Australia | Singapore | Virginia | Oregon", False),
                  ("CPU:", "Intel(R) Core(TM) i7-7700K CPU @ 4.20GHz", True),
                  ("RAM:", "DDR4 2400 MHz", True),
                  ("MySQL DB:", "Free", False),
                  ("Unlimited Slots:", "Free", True),
                  ("Subdomain:", "Free", True)]

        premium.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        premium.set_footer(text="Page 1 of 2")

        for name, value, inline in fields:
            premium.add_field(name=name, value=value, inline=inline)
     
        standard = discord.Embed(title="-- Standard --", 
                      color=discord.Colour.blue())

        fields = [("Price/mo:", "$3/GB", False),
                  ("Locations:", "Canada | France", False),
                  ("CPU:", "Intel(R) Xeon(R) CPU E5-1630 v4 @ 3.70GHz", True),
                  ("RAM:", "DDR4 2133 MHz", True),
                  ("MySQL DB:", "$2/mo Addon", False),
                  ("Unlimited Slots:", "$2 Addon", True),
                  ("Subdomain:", "Free", True)]

        standard.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        standard.set_footer(text="Page 2 of 2")

        for name, value, inline in fields:
            standard.add_field(name=name, value=value, inline=inline)

        pages = [premium, standard]

        await menu(ctx, pages, DEFAULT_CONTROLS)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def plans(self, ctx):
        """
            Shows all our plans.
        """
        stone = discord.Embed(title="Stone Plan", description="[OUR PLANS](https://ggservers.com/minecrafthosting)", color=discord.Colour.blue())

        fields = [("Price:", "$3/mo", True),
                  ("Ram:", "1GB", True),
                  ("Slots:", "12 Total", True),
                  ("Recommended Players in One Instance:", "4 Total", False),
                  ("Plugins:", "0", False),
                  ("Mods:", "0", True)]

        stone.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        stone.set_thumbnail(url="https://ggservers.com/images/stone.png")
        stone.set_footer(text="Page 1 of 8")

        for name, value, inline in fields:
            stone.add_field(name=name, value=value, inline=inline)

        coal = discord.Embed(title="Coal Plan", description="[OUR PLANS](https://ggservers.com/minecrafthosting)", color=discord.Colour.blue())

        fields = [("Price:", "$6/mo", True),
                  ("Ram:", "2GB", True),
                  ("Slots:", "24 Total", True),
                  ("Recommended Players in One Instance:", "8 Total", False),
                  ("Plugins:", "8", False),
                  ("Mods:", "8", True)]

        coal.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        coal.set_thumbnail(url="https://ggservers.com/images/coal.png")
        coal.set_footer(text="Page 2 of 8")

        for name, value, inline in fields:
            coal.add_field(name=name, value=value, inline=inline)

        iron = discord.Embed(title="Iron Plan", description="[OUR PLANS](https://ggservers.com/minecrafthosting)", color=discord.Colour.blue())

        fields = [("Price:", "$9/mo", True),
                  ("Ram:", "3GB", True),
                  ("Slots:", "36 Total", True),
                  ("Recommended Players in One Instance:", "16 Total", False),
                  ("Plugins:", "24", False),
                  ("Mods:", "24", True)]

        iron.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        iron.set_thumbnail(url="https://ggservers.com/images/iron.png")
        iron.set_footer(text="Page 3 of 8")

        for name, value, inline in fields:
            iron.add_field(name=name, value=value, inline=inline)

        gold = discord.Embed(title="Gold Plan", description="[OUR PLANS](https://ggservers.com/minecrafthosting)", color=discord.Colour.blue())

        fields = [("Price:", "$12/mo", True),
                  ("Ram:", "4GB", True),
                  ("Slots:", "48 Total", True),
                  ("Recommended Players in One Instance:", "20 Total", False),
                  ("Plugins:", "36", False),
                  ("Mods:", "36", True)]

        gold.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        gold.set_thumbnail(url="https://ggservers.com/images/gold.png")
        gold.set_footer(text="Page 4 of 8")

        for name, value, inline in fields:
            gold.add_field(name=name, value=value, inline=inline)

        lapis = discord.Embed(title="Lapis Plan", description="[OUR PLANS](https://ggservers.com/minecrafthosting)", color=discord.Colour.blue())

        fields = [("Price:", "$15/mo", True),
                  ("Ram:", "5GB", True),
                  ("Slots:", "60 Total", True),
                  ("Recommended Players in One Instance:", "24 Total", False),
                  ("Plugins:", "44", False),
                  ("Mods:", "44", True)]

        lapis.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        lapis.set_thumbnail(url="https://ggservers.com/images/lapis.png")
        lapis.set_footer(text="Page 5 of 8")

        for name, value, inline in fields:
            lapis.add_field(name=name, value=value, inline=inline)

        redstone = discord.Embed(title="Redstone Plan", description="[OUR PLANS](https://ggservers.com/minecrafthosting)", color=discord.Colour.blue())

        fields = [("Price:", "$18/mo", True),
                  ("Ram:", "6GB", True),
                  ("Slots:", "72 Total", True),
                  ("Recommended Players in One Instance:", "40 Total", False),
                  ("Plugins:", "52", False),
                  ("Mods:", "52", True)]

        redstone.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        redstone.set_thumbnail(url="https://ggservers.com/images/redstone.png")
        redstone.set_footer(text="Page 6 of 8")

        for name, value, inline in fields:
            redstone.add_field(name=name, value=value, inline=inline)

        diamond = discord.Embed(title="Diamond Plan", description="[OUR PLANS](https://ggservers.com/minecrafthosting)", color=discord.Colour.blue())

        fields = [("Price:", "$24/mo", True),
                  ("Ram:", "8GB", True),
                  ("Slots:", "96 Total", True),
                  ("Recommended Players in One Instance:", "80 Total", False),
                  ("Plugins:", "64+", False),
                  ("Mods:", "62+", True)]

        diamond.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        diamond.set_thumbnail(url="https://ggservers.com/images/diamond.png")
        diamond.set_footer(text="Page 7 of 8")

        for name, value, inline in fields:
            diamond.add_field(name=name, value=value, inline=inline)

        emerald = discord.Embed(title="Emerald Plan", description="[OUR PLANS](https://ggservers.com/minecrafthosting)", color=discord.Colour.blue())

        fields = [("Price:", "$36/mo", True),
                  ("Ram:", "12GB", True),
                  ("Slots:", "144 Total", True),
                  ("Recommended Players in One Instance:", "120+ Total", False),
                  ("Plugins:", "72+", False),
                  ("Mods:", "72+", True)]

        emerald.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        emerald.set_thumbnail(url="https://ggservers.com/images/emerald.png")
        emerald.set_footer(text="Page 8 of 8")

        for name, value, inline in fields:
            emerald.add_field(name=name, value=value, inline=inline)

        pages = [stone, coal, iron, gold, lapis, redstone, diamond, emerald]

        await menu(ctx, pages, DEFAULT_CONTROLS)
   
    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def luckperms(self, ctx):
        """
            Displays all relevant luckperms information.
        """
        luckperms = discord.Embed(title="Luckperms Setup", description="[DOWNLOAD HERE](https://luckperms.net/download)", color=discord.Colour.blue())

        fields = [("Change Server Type | Bukkit, Spigot, Paper:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-change-your-server-type-and-version-ve6dtm/)", False),
                  ("Installation of Luckperms:", "[Knowledgebase](https://help.ggservers.com/en-us/article/luckperms-installation-setup-9eqlef/)", False),
                  ("OP Yourself:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-op-yourself-on-your-minecraft-server-1l4zakc/)", False),
                  ("Luckperms Usage:", "[WIKI](https://luckperms.net/wiki/Home)", False)]

        luckperms.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        luckperms.set_thumbnail(url="https://storage.crisp.chat/users/helpdesk/website/ba33bb39ceb6d800/lp_4o1qyq.png")

        for name, value, inline in fields:
            luckperms.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=luckperms)


    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def allbackup(self, ctx):
        """
            Shows all information needed for backups.
        """
        backup = discord.Embed(title="All about Backups", description="[Access Multicraft](https://mc.ggservers.com/)", color=discord.Colour.blue())

        fields = [("Difference between Autosaves & Backups:", "[HERE](https://help.ggservers.com/en-us/article/whats-the-difference-between-an-autosave-and-a-backup-ww1jlw/)", False),
                  ("Make Backup + Download:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-make-a-backup-and-download-it-noz1kf/)", False),
                  ("Creating Automatic Backup Task:", "[Knowledgebase](https://help.ggservers.com/en-us/article/create-automatic-backup-1rqhzrp/)", False),
                  ("Restore Backup:", "[Knowledgebase](https://help.ggservers.com/en-us/article/restoring-a-backup-1t4rbqw/)", False)]

        backup.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        backup.set_thumbnail(url="https://i.imgur.com/pFjrQbQ.png")

        for name, value, inline in fields:
            backup.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=backup)


    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def allftp(self, ctx):
        """
            Shows Filezilla, WinSCP and Multicraft ftp usage and information.
        """
        ftp = discord.Embed(title="Filezilla | WinSCP | Multicraft FTP", description="FTPs to Access your server files", color=discord.Colour.blue())

        fields = [("Filezilla Client:", "[Download](https://filezilla-project.org/download.php?type=client)", True),
                  ("WinSCP Client:", "[Download](https://winscp.net/eng/download.php)", True),
                  ("Multicraft FTP:", "[HERE](https://mc.ggservers.com/)", True),
                  ("Filezilla Usage:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-connect-to-your-server-using-filezilla-yl0q5r/)", True),
                  ("WinSCP Usage:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-connect-with-winscp-rfcman/)", True),
                  ("Multicraft FTP Usage:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-access-your-minecraft-server-files-via-ftp-18ealdp/)", True)]

        ftp.set_author(name="GGServers", icon_url=ctx.guild.icon_url)
        ftp.set_thumbnail(url="https://imgur.com/LYmUGdT.png")

        for name, value, inline in fields:
            ftp.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=ftp)


    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def allupgrade(self, ctx):
        """
            Shows information about upgrades.
        """
        upgrade = discord.Embed(title="Upgrade/Downgrade Service", description="[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-upgrade-or-downgrade-your-service-1yowxis/)", color=discord.Colour.blue())

        fields = [("Ram:", "[Billing Area](http://ggservers.com/billing)", True),
                  ("Standard | Premium:", "You will need to open a ticket to billing department requesting it.", True),
                  ("Ticket - Login to GGServers Account:", "[Click Here](https://ggservers.com/billing/submitticket.php)", False)]

        upgrade.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            upgrade.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=upgrade)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def multialts(self, ctx):
        """
            Show Multicraft alternate links.
        """
        embed = discord.Embed(title="Alternate Multicraft Links", description="[MC1](https://mc1.ggservers.com) | [MC2](https://mc2.ggservers.com)  | [MC3](https://mc3.ggservers.com) | [MC4](https://mc4.ggservers.com)", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def refund(self, ctx):
        """
            Shows our refund policy information.
        """
        embed = discord.Embed(title="Refund", description="How to get a refund on your service", color=discord.Colour.blue())

        fields = [("Reimbursement Policy:", "We can only offer a refund for a service if the request was made within 24 hours of purchase.", False),
                  ("Ticket | Billing Department:", "[HERE](https://ggservers.com/billing/submitticket.php) | Login to your GGServers Account", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def native(self, ctx):
        """
            Shows memory error information.
        """
        native = discord.Embed(title="Native Error", description="## There is insufficient memory for the Java Runtime Environment to continue.", color=discord.Colour.blue())

        fields = [("Solution:", "Open a ticket to the Node Transfer department", False),
                  ("Open Ticket:", "[HERE](https://ggservers.com/billing/submitticket.php) | Login to your GGServers Account", False)]

        native.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            native.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=native)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def modsplugins(self, ctx):
        """
            Shows anything mods & plugins related.
        """
        modsplugins = discord.Embed(title="Mods & Plugins", description="By default, modded servers don't support Bukkit plugins because mods aren't based on Vanilla Minecraft. In this case, you can use Spongeforge plugins on your modded server, to run sponge plugins on 1.12.2.", color=discord.Colour.blue())

        fields = [("Guide:", "[Knowledgebase](https://help.ggservers.com/en-us/article/understanding-servers-using-mods-and-plugins-at-the-same-time-1ko7ils/)", False),
                  ("Alternatives to Sponge:", "[Magma](https://help.ggservers.com/en-us/article/magma-installation-szippb/) | [Mohist](https://help.ggservers.com/en-us/article/mohist-installation-3meexc/)", False),
                  ("Note:", "These two have lots of crash and instability issues as mods and plugins are not supposed to run together.", False)]

        modsplugins.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            modsplugins.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=modsplugins)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def performance(self, ctx):
        """
            Shows all performance related articles.
        """
        embed = discord.Embed(title="Server Performance", description="These articles will help you understand and resolve perfomance issues.", color=discord.Colour.blue())

        fields = [("Improve Server Performance:", "[Knowledgebase](https://help.ggservers.com/en-us/article/improve-your-server-performance-e73vt3/)", False),
                  ("Improve Modded Server Performance:", "[Knowledgebase](https://help.ggservers.com/en-us/article/improve-your-forge-modded-server-performance-no7k8k/)", False),
                  ("Check Server Performance:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-check-your-server-performance-1w9bovl/)", False),
                  ("MC 1.16x Changes & Performance Issues:", "[Knowledgebase](https://help.ggservers.com/en-us/article/minecraft-116x-changes-performance-issues-51zlmu/)", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def resetpass(self, ctx):
        """
            Shows all password reset guides.
        """
        embed = discord.Embed(title="Multicraft/Billing Password Reset", description="These articles help you to reset your passwords.", color=discord.Colour.blue())

        fields = [("Multicraft Password:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-reset-your-multicraft-password-sqa3sf/)", False),
                  ("Billing Area Password:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-reset-your-billing-area-password-1ik6zm5/)", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def custom(self, ctx):
        """
            Shows custom installation guides.
        """
        embed = discord.Embed(title="Custom Jar | Forge | Resource Pack", description="These articles are to implement custom features on your server.", color=discord.Colour.blue())

        fields = [("Custom Jar:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-upload-and-use-a-custom-jar-file-1kzlntv/)", False),
                  ("Custom Forge:", "[Knowledgebase](https://help.ggservers.com/en-us/article/custom-forge-installation-1u6gex2/)", False),
                  ("Custom Resource Pack:", "[Knowledgebase](https://help.ggservers.com/en-us/article/implement-a-custom-resource-texture-pack-in-your-server-gx8viz/)", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def allworld(self, ctx):
        """
            Shows all world related guides.
        """
        embed = discord.Embed(title="Minecraft Worlds", description="These articles are for world creation and implementation.", color=discord.Colour.blue())

        fields = [("Upload World:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-upload-a-world-to-your-server-2g0nyj/)", True),
                  ("Upload World | Bedrock:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-upload-your-custom-world-on-a-bedrock-server-bwwamw/)", True),
                  ("Create New World:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-create-a-new-world-2fh26b/)", False),
                  ("Generate Flat World:", "[Knowledgebase](https://help.ggservers.com/en-us/article/generating-a-flat-world-g0nadv/)", False),
                  ("Pre-Generate World:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-pre-generate-your-world-1uqqhq6/)", False),
                  ("Download World:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-download-your-world-17ewr1r/)", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def worldmgmt(self, ctx):
        """
            Shows all world management guides.
        """
        embed = discord.Embed(title="World Management", description="These articles are for managing your Minecraft worlds.", color=discord.Colour.blue())

        fields = [("World Border:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-upload-a-world-to-your-server-2g0nyj/)", False),
                  ("WorldBorder Plugin:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-upload-your-custom-world-on-a-bedrock-server-bwwamw/)", False),
                  ("View & Change World Seed:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-view-and-change-your-world-seed-3vzj0b/)", False),
                  ("WorldEdit Installation:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-download-your-world-17ewr1r/)", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def fabric(self, ctx):
        """
            Shows fabric guide.
        """
        embed = discord.Embed(title="Fabric MC", description="Fabric is a Custom Jar File modded-friendly that usually helps some Modpacks in their performance as well as dependency for specified mods.", color=discord.Colour.blue())

        fields = [("Fabric Download:", "[HERE](https://fabricmc.net/use/)", False),
                  ("Fabric Installation:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-install-fabric-in-your-minecraft-server-nwle1r/)", False),
                  ("Fabric Usage:", "[Wiki](https://fabricmc.net/wiki/doku.php)", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def daemon(self, ctx):
        """
            Daemon issue related
        """
        embed = discord.Embed(title="Daemon 110/111", 
                              description="This is an error on our end, no worries.\nFor record-keeping purposes, you can head over to <#686284042873864205> to report it.", color=discord.Colour.blue())

        fields = [("Daemon 110:", "System Administrators are working on resolving the issue.", False),
                  ("Daemon 111:", "Mostly temporary performance maintainence.", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def cmds(self, ctx):
        """
            Vanilla/Custom Commands.
        """
        embed = discord.Embed(title="Minecraft Commands", description="These articles will guide you through general commands.", color=discord.Colour.blue())

        fields = [("Vanilla Commands:", "[Knowledgebase](https://help.ggservers.com/en-us/article/vanilla-commands-11xx8gv/)", False),
                  ("Custom Commands:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-create-custom-commands-using-the-multicraft-panel-1p3hnl/)", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def biomesop(self, ctx):
        """
            Biomes O. Plenty Mod Info.
        """
        embed = discord.Embed(title="Biomes O' Plenty | Forge Modded Servers", description="Installation & Information", color=discord.Colour.blue())

        fields = [("BiomesOP Download:", "[HERE](https://www.curseforge.com/minecraft/mc-mods/biomes-o-plenty/files)", False),
                  ("Installation | Usage:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-set-up-and-use-biomes-o-plenty-mod-1kuwpqm/)", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def tebex(self, ctx):
        """
            TEBEX - Buycraft Setup
        """
        embed = discord.Embed(title="TEBEX - Buycraft Setup", description="[Knowledgebase](https://help.ggservers.com/en-us/article/tebex-buycraft-setup-sr580/)", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def plugins(self, ctx):
        """
            Plugin Installation Information.
        """
        embed = discord.Embed(title="Plugins Installation", description="First, you have to be sure that your server is running on Spigot, CraftBukkit or PaperSpigot! Vanilla can't run plugins.", color=discord.Colour.blue())

        fields = [("Change Server Type/Version:", "[Knowledgebase](https://help.ggservers.com/en-us/article/change-your-server-version-ve6dtm/)", False),
                  ("Installation:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-install-plugins-on-your-server-1yxw90a/)", False),
                  ("Recommended Plugins:", "[Knowledgebase](https://help.ggservers.com/en-us/article/bukkit-spigot-paperspigot-recommended-plugins-f0k0g9/)", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def cc3(self, ctx):
        """
            Crazycraft 3.0 Not Working.
        """
        embed = discord.Embed(title="Crazy Craft 3.0", description="The Crazy Craft 3.0 is not working due to the files distributed by the creator of the modpack. We can not do anything about this.", color=discord.Colour.blue())

        fields = [("Solution:", "We offer Crazy Craft 2.2. All you have to do is a clean install of 'VoidCrazyCraft' template to obtain the 2.2 version into your server.", False),
                  ("Clean Installation:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-install-any-server-type-from-our-list-133ufiy/)", False),
                  ("Note:", "This process will delete all your server files so backup what you need first to your PC", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def scramble(self, ctx):
        """
            Turn scrambled recipes off.
        """
        embed = discord.Embed(title="Turn scrambled recipes off", description="To remove the scrambled recipes you need to use the command /gamerule scramblerecipes false", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def ticketbedrock(self, ctx):
        """
            Ticket for bedrock node move.
        """
        embed = discord.Embed(title="Ticket for Bedrock Node", description="Your server needs to be moved to a bedrock node. You can open a ticket here and request a move to a Bedrock Node.", color=discord.Colour.blue())

        fields = [("Open Ticket:", "[HERE](https://ggservers.com/billing/submitticket.php) | Login to GGServers Account", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def bedrock(self, ctx):
        """
            Bedrock Information.
        """
        embed = discord.Embed(title="Bedrock Server Information", description="These articles are for Bedrock Servers.", color=discord.Colour.blue())

        fields = [("Bedrock Introduction:", "[Knowledgebase](https://help.ggservers.com/en-us/article/bedrock-dedicated-introduction-14c2u1u/)", False),
                  ("Show Coordinates:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-turn-on-show-coordinates-option-on-my-bedrock-server-1jlvg60/)", False),
                  ("Connect to Bedrock Server | Xbox & Switch:", "[Knowledgebase](https://help.ggservers.com/en-us/article/connect-to-a-bedrock-server-using-xbox-and-nintendo-switch-w15pfr/)", False),
                  ("Upload World | Bedrock:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-upload-your-custom-world-on-a-bedrock-server-bwwamw/)", False),
                  ("Geyser Plugin Setup:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-set-up-and-use-geyser-plugin-1p8eyyi/)", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def logs(self, ctx):
        """
            Logs in chat.
        """
        embed = discord.Embed(title="Console/Crash Logs", 
                              description="Go to your console in [Multicraft](https://mc.ggservers.com/).\n"
                                          "Select the entire console.\n"
                                          "Copy it.\n"
                                          "Paste the logs [Here](https://paste.gg/).\n"
                                          "Click on Submit.\n"
                                          "Copy the web address URL from the address bar.\n"
                                          "Paste it in <#663561950130601995>.\n", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def multidown(self, ctx):
        """
            Multicraft Down.
        """
        embed = discord.Embed(title="Multicraft Down | Error 500", 
                              description="Staff members are aware of the issue right now. Thank you for reporting it. They're working on a fix as we speak. Appreciate the patience, and sincere apologies for the inconvenience.", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def clearcache(self, ctx):
        """
            Error 524.
        """
        embed = discord.Embed(title="Clear Browser Cache/Cookies", 
                              description="Please go to the page, press the padlock on the address bar, click cookies, then remove them all, click done, then refresh the page, this should fix the problem. If these instructions don't work for you, please clear the cookies / cache of your browser.", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def eta(self, ctx):
        """
            ETA on tickets. 
        """
        embed = discord.Embed(title="Ticket Response Time", 
                              description="Staff do tickets in order of them being received. You will receive a response once it has been resolved. Your patience is appreciated!", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def customdomain(self, ctx):
        """
            Setting up custom domains for servers. 
        """
        embed = discord.Embed(title="Custom Domains", 
                              description="Use a Custom Domain with your server.", color=discord.Colour.blue())

        fields = [("NameCheap:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-use-a-custom-domain-url-with-your-server-using-namecheap-1yd13x8/)", False),
                  ("Google Domains:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-use-a-custom-domain-url-with-your-server-using-google-domains-cdcgpb/)", False),
                  ("GoDaddy:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-use-a-custom-domain-url-with-your-server-using-godaddy-ekdj7q/)", False),
                  ("Cloudflare:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-adding-a-custom-domain-url-with-cloudfare-1sw9uel/)", False)] 

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def clean(self, ctx):
        """
            Clean installation. 
        """
        embed = discord.Embed(title="Clean Installation", 
                              description="[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-install-any-server-type-clean-installation-133ufiy/)", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def fly(self, ctx):
        """
            Flying is not enabled. 
        """
        embed = discord.Embed(title="Flying is not Enabled", 
                              description="[Knowledgebase](https://help.ggservers.com/en-us/article/flying-is-not-enabled-on-this-server-18544oc/)", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def mods(self, ctx):
        """
            Mods installation. 
        """
        embed = discord.Embed(title="Mods Installation", 
                              description="These articles will guide you through installing mods on your server and client.", color=discord.Colour.blue())

        fields = [("Clean Installation:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-install-any-server-type-clean-installation-133ufiy/)", False),
                  ("Install Mods | Server:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-install-mods-on-your-server-1bauy2t/)", False),
                  ("Install Mods | Client:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-install-mods-into-your-client-1t47nya/)", False),
                  ("Edit Mod Config Files:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-edit-mod-configuration-files-twetns/)", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def watchdog(self, ctx):
        """
            Disables watchdog. 
        """
        embed = discord.Embed(title="Watchdog Error", 
                              description="1 - Stop the server.\n"
                                          "2 - Go Files > Config Files > Server settings.\n"
                                          "3 - Change the Max tick time to -10000.\n"
                                          "4 - Save it.\n"
                                          "5 - Start the server again.", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def whitelisting(self, ctx):
        """
            Whitelist setup. 
        """
        embed = discord.Embed(title="Whitelist Setup", 
                              description="These articles will guide you through setting up a whitelist for your server.", color=discord.Colour.blue())

        fields = [("Java Edition:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-use-the-minecraft-whitelist-1nw0h6e/)", False),
                  ("Bedrock Edition:", "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-use-the-whitelist-on-your-bedrock-server-4dpjed/)", False)]

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def credentials(self, ctx):
        """
            Multicraft credentials. 
        """
        embed = discord.Embed(title="Multicraft Credentials", 
                              description="Please check your email for one titled **Your Minecraft Server Details**.\n"
                                          "This will contain your login credentials for Multicraft, as well as the connection info for your server.", color=discord.Colour.blue())

        fields = [("You can view it here:", "[Client Area](https://ggservers.com/billing/clientarea.php?action=emails)", False)]


        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def ticking(self, ctx):
        """
            Ticking entity. 
        """
        embed = discord.Embed(title="Ticking Entity Error", 
                              description="A Ticking Entity is a mob/creature/NPC that had become corrupt in your world.\n"
                                          "[Knowledgebase](https://help.ggservers.com/en-us/article/ticking-entity-what-is-and-how-to-avoid-it-1yjzxl7/)", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def entitypurge(self, ctx):
        """
            Entity purge tool. 
        """
        embed = discord.Embed(title="Entity Purge Tool", 
                              description="This article will show you how you can properly erase all entities from your server.\n"
                                          "This is usually needed when you are experiencing a ticking entity error or ticking world error.\n"
                                          "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-erase-all-entities-from-your-server-rlq1kl/)", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def jsonvalidator(self, ctx):
        """
            JSON Validator usage. 
        """
        embed = discord.Embed(title="JSON Validator", 
                              description="This article will explain to you what a JSON Validator is, and how to use it to identify and solve a JSON error type.\n"
                                          "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-use-the-json-validator-json-error-type-12ugkgp/)", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def openport(self, ctx):
        """
            Open port for plugins. 
        """
        embed = discord.Embed(title="Finding an Open Port for Plugins", 
                              description="This guide will show you how to find an open port for any plugin that needs an extra one.\n"
                                          "[Knowledgebase](https://help.ggservers.com/en-us/article/how-to-find-an-open-port-for-your-plugin-od9adt/)", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(whitelist)
    @has_permissions(manage_messages=True)
    async def cancel(self, ctx):
        """
            Cancel your service. 
        """
        embed = discord.Embed(title="Cancel Your Service", 
                              description="These articles will show you how to cancel your service.\n"
                                          "[Cancel Service](https://help.ggservers.com/en-us/article/how-to-cancel-your-service-1vjbohv/)\n"
                                          "[Cancel PayPal Subscription](https://help.ggservers.com/en-us/article/how-to-cancel-your-paypal-subscription-nocjy5/)", color=discord.Colour.blue())

        embed.set_author(name="GGServers", icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)
