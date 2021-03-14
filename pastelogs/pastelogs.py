import discord
import asyncio

from synergy.core import commands, checks, Config


class PasteLogs(commands.Cog):

    """Automated replies when trigger words in logs are sent in chat.
       Still very much under development. But the logic is shown, and works."""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        
        self.pastelogs = self.bot.get_channel(814998380228247582)

        # Checks if messages are sent in the logs channel. To prevent response to other channels.
        # Also prevents clogging up the paste-logs channel. 

        if message.channel == self.pastelogs:
            pass
        else:
            return

        if not message.guild:
            return

        if message.author == self.bot.user:
            return

        error1 = [
                    "insufficient memory", 
                    "Native memory allocation",
                    "Java Runtime Environment",
                    "[Server] INFO java.lang.OutOfMemoryError"
                  ]

        for error in error1:
            if error.lower() in message.content.lower():

                response = discord.Embed(title="Not enough RAM", 
                                         description="Open a ticket titled: **Native Error** | [HERE](https://ggservers.com/billing/submitticket.php)",
                                         color=discord.Colour.blue())

                await message.channel.send(embed=response, delete_after=30.0)
                return await message.delete()

        error2 = [
                    "failed to bind to port!", 
                    "perhaps a server is already running on that port?"
                  ]

        for error in error2:
            if error.lower() in message.content.lower():

                response = discord.Embed(title="Solution for Errors", 
                                         description="Open a ticket titled: **Failed to bind to port** | [HERE](https://ggservers.com/billing/submitticket.php)",
                                         color=discord.Colour.blue())

                await message.channel.send(embed=response, delete_after=30.0)
                return await message.delete()

        error3 = [
                    "Can't connect to daemon (110: Connection Timed out)"
                  ]

        for error in error3:
            if error.lower() in message.content.lower():

                response = discord.Embed(title="Daemon Issue (110)", 
                                         description="Hey there! Staff members are well aware of it and System Administrators are working to resolve the issue. You can report it in <#686284042873864205>.",
                                         color=discord.Colour.blue())

                await message.channel.send(embed=response, delete_after=30.0)
                return await message.delete()

        error4 = [
                    "Can't connect to daemon (111: Connection Refused)" 
                  ]

        for error in error4:
            if error.lower() in message.content.lower():

                response = discord.Embed(title="Daemon Issue (111)", 
                                         description="Hey there! This is usually due to temporary performance maintainence on our end. It will be back up shortly! You can report it in <#686284042873864205>.",
                                         color=discord.Colour.blue())

                await message.channel.send(embed=response, delete_after=30.0)
                return await message.delete()

        error5 = [
                    "Server thread/WARN Can't keep up! Is the server overloaded? " 
                  ]

        for error in error5:
            if error.lower() in message.content.lower():

                response = discord.Embed(title="High Resource Usage", 
                                         description="Staff can move you to a fresher node which should resolve these performance issues. Open ticket [HERE](https://ggservers.com/billing/submitticket.php).",
                                         color=discord.Colour.blue())

                await message.channel.send(embed=response, delete_after=30.0)
                return await message.delete()

        error6 = [
                    "Couldn't load chunk - java.lang.NullPointerException" 
                  ]

        for error in error6:
            if error.lower() in message.content.lower():

                response = discord.Embed(title="Chunk(s) Corrupted", 
                                         description="We recommend either restoring a backup [HERE](https://help.ggservers.com/en-us/article/how-to-restore-a-backup-1t4rbqw/).\n"
                                                     "OR\n" 
                                                     "Creating a new world [HERE](https://help.ggservers.com/en-us/article/how-to-create-a-new-world-2fh26b/)",
                                                     color=discord.Colour.blue())

                await message.channel.send(embed=response, delete_after=30.0)
                return await message.delete()

        error7 = [
                    "[Server] INFO FATAL ERROR, You need to run the installer. The libraries required to launch a server are missing" 
                  ]

        for error in error7:
            if error.lower() in message.content.lower():

                response = discord.Embed(title="Missing Libraries Solution", 
                                         description="1. Click on **Files** and select **Setup**.\n"
                                                     "2. Select the template (Server Type/ModPack) you want to use.\n"
                                                     "3. Tick the box for **Delete All Server Files**. Save it.\n"
                                                     "4. Go back and start/restart your server up!",
                                                     color=discord.Colour.blue())

                response.set_footer(text="If you need any files, please back them up into your computer using FileZilla, as this will remove everything including backups!")

                await message.channel.send(embed=response, delete_after=30.0)
                return await message.delete()

        error8 = [
                    "Duplicate Mods" 
                  ]

        for error in error8:
            if error.lower() in message.content.lower():

                response = discord.Embed(title="Duplicate Mods", 
                                         description="You have duplicate mods running on your server, please remove any duplicate mods and it will be up and running again.",
                                                     color=discord.Colour.blue())

                await message.channel.send(embed=response, delete_after=30.0)
                return await message.delete()

        error9 = [
                    "fml.common.MissingModsException" 
                  ]

        for error in error9:
            if error.lower() in message.content.lower():

                response = discord.Embed(title="Mod Dependencies Missing", 
                                         description="One of your mods is missing one or more dependency mods that it needs to be able to run. It should say in the error what mods are needed. Install those.\n"
                                                     "[Open Guide](https://help.ggservers.com/en-us/article/how-to-install-mods-on-your-server-1bauy2t/)",
                                                     color=discord.Colour.blue())

                await message.channel.send(embed=response, delete_after=30.0)
                return await message.delete()

        error10 = [
                    "reason: Failed to verify username!" 
                  ]

        for error in error10:
            if error.lower() in message.content.lower():

                response = discord.Embed(title="Failed To Verify Username", 
                                         description="This is a common error that you may receive when you try to join your server.\n"
                                                     "[Open Guide](https://help.ggservers.com/en-us/article/failed-to-verify-username-wnecbr/)",
                                                     color=discord.Colour.blue())

                await message.channel.send(embed=response, delete_after=30.0)
                return await message.delete()

