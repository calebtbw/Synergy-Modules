import discord
import aiohttp

from bs4 import BeautifulSoup
from datetime import datetime
from synergy.core import commands


site = 'https://status.ggservers.com/'

# WIP: Going to make this crawl the entire status website to extract all the links
# in accordance with the node ID provided, and display data accordingly. 
class NodeStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.group(aliases=["ns"])
    async def nodestatus(self, ctx):
        """Retrieves Node Status from status.ggservers.com"""
        pass
    
    # Testing
    @nodestatus.command()
    async def d1(self, ctx):
        progress = await ctx.send(
            "Retrieving data..."
        )
        sess = aiohttp.ClientSession()
        req = await sess.get('https://status.ggservers.com/report/uptime/90ce21d81c4a651a4aac96f2f9bbd5f2/')

        soup = BeautifulSoup(await req.read(), 'html.parser')
        results = soup.find(id='reportuptimecontainer')
        stats = results.find_all('div', class_='page-content')

        for stat in stats:
            uptime_elem = stat.find('div', class_='number')
            change_elem = stat.find('div', class_='desc')
            if None in (uptime_elem, change_elem):
                continue
            
            uptime = uptime_elem.text
            change = change_elem.text
                         
            e = discord.Embed(
                title="Node Status", 
                description=f"Node ID: 1 | NA Standard",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
                )
            e.add_field(name="Status:", value=uptime)
            e.add_field(name="Changes:", value=change)
            e.set_thumbnail(url=ctx.guild.icon_url)
            e.set_footer(text=f"Retreived from {site}")

            await progress.edit(content="Data successfully retrieved.")
            return await ctx.send(embed=e)
    # End Testing

    # Start Premium Singapore
    @nodestatus.command()
    async def d122(self, ctx):
        progress = await ctx.send(
            "Retrieving data..."
        )
        sess = aiohttp.ClientSession()
        req = await sess.get('https://status.ggservers.com/report/uptime/cc2ca46d84c2a3f49ac8e287f4f9e99d/')

        soup = BeautifulSoup(await req.read(), 'html.parser')
        results = soup.find(id='reportuptimecontainer')
        stats = results.find_all('div', class_='page-content')

        for stat in stats:
            uptime_elem = stat.find('div', class_='number')
            change_elem = stat.find('div', class_='desc')
            if None in (uptime_elem, change_elem):
                continue
            
            uptime = uptime_elem.text
            change = change_elem.text
                         
            e = discord.Embed(
                title="Node Status", 
                description=f"Node ID: 122 | Premium Singapore",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
                )
            e.add_field(name="Status:", value=uptime)
            e.add_field(name="Changes:", value=change)
            e.set_thumbnail(url=ctx.guild.icon_url)
            e.set_footer(text=f"Retreived from {site}")

            await progress.edit(content="Data successfully retrieved.")
            return await ctx.send(embed=e)

    @nodestatus.command()
    async def d323(self, ctx):
        progress = await ctx.send(
            "Retrieving data..."
        )
        sess = aiohttp.ClientSession()
        req = await sess.get('https://status.ggservers.com/report/uptime/fe3b714fee4403bb8a762db035b4edbe/')

        soup = BeautifulSoup(await req.read(), 'html.parser')
        results = soup.find(id='reportuptimecontainer')
        stats = results.find_all('div', class_='page-content')

        for stat in stats:
            uptime_elem = stat.find('div', class_='number')
            change_elem = stat.find('div', class_='desc')
            if None in (uptime_elem, change_elem):
                continue
            
            uptime = uptime_elem.text
            change = change_elem.text
                         
            e = discord.Embed(
                title="Node Status", 
                description=f"Node ID: 323 | Premium Singapore",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
                )
            e.add_field(name="Status:", value=uptime)
            e.add_field(name="Changes:", value=change)
            e.set_thumbnail(url=ctx.guild.icon_url)
            e.set_footer(text=f"Retreived from {site}")

            await progress.edit(content="Data successfully retrieved.")
            return await ctx.send(embed=e)

    @nodestatus.command()
    async def d700(self, ctx):
        progress = await ctx.send(
            "Retrieving data..."
        )
        sess = aiohttp.ClientSession()
        req = await sess.get('https://status.ggservers.com/report/uptime/efe99d064ada0de3f823fa1e4e8febcb/')

        soup = BeautifulSoup(await req.read(), 'html.parser')
        results = soup.find(id='reportuptimecontainer')
        stats = results.find_all('div', class_='page-content')

        for stat in stats:
            uptime_elem = stat.find('div', class_='number')
            change_elem = stat.find('div', class_='desc')
            if None in (uptime_elem, change_elem):
                continue
            
            uptime = uptime_elem.text
            change = change_elem.text
                         
            e = discord.Embed(
                title="Node Status", 
                description=f"Node ID: 700 | Premium Singapore",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
                )
            e.add_field(name="Status:", value=uptime)
            e.add_field(name="Changes:", value=change)
            e.set_thumbnail(url=ctx.guild.icon_url)
            e.set_footer(text=f"Retreived from {site}")

            await progress.edit(content="Data successfully retrieved.")
            return await ctx.send(embed=e)

    @nodestatus.command()
    async def d771(self, ctx):
        progress = await ctx.send(
            "Retrieving data..."
        )
        sess = aiohttp.ClientSession()
        req = await sess.get('https://status.ggservers.com/report/uptime/1f831a7d202bfad3e0b2b1cdde1a31c9/')

        soup = BeautifulSoup(await req.read(), 'html.parser')
        results = soup.find(id='reportuptimecontainer')
        stats = results.find_all('div', class_='page-content')

        for stat in stats:
            uptime_elem = stat.find('div', class_='number')
            change_elem = stat.find('div', class_='desc')
            if None in (uptime_elem, change_elem):
                continue
            
            uptime = uptime_elem.text
            change = change_elem.text
                         
            e = discord.Embed(
                title="Node Status", 
                description=f"Node ID: 771 | Premium Singapore",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
                )
            e.add_field(name="Status:", value=uptime)
            e.add_field(name="Changes:", value=change)
            e.set_thumbnail(url=ctx.guild.icon_url)
            e.set_footer(text=f"Retreived from {site}")

            await progress.edit(content="Data successfully retrieved.")
            return await ctx.send(embed=e)           
    # End Premium Singapore
