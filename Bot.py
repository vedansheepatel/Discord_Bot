import discord 
import Search
import trending
import recommendations
from dotenv import load_dotenv
load_dotenv()

import os
from discord.ext import commands
intents = discord.Intents.all()
client = discord.Client(intents=intents) 

bot_cmds={}
bot_cmds['$search [name]'] = ' get information about a certain drama/movie'
bot_cmds['$recs [name]'] = ' get recommendations for shows similar to a certain drama/movie'
bot_cmds['$trending'] = ' see the Top 10 trending shows/movies at the moment'

@client.event
async def on_ready():
	print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("$hello"):
        await message.channel.send("Hello "+ message.author.name + '!')
    
    if message.content.startswith('$search '):
        
        drama_link = Search.search_drama(message.content)
        drama_data = Search.get_data(drama_link)
        if 'drama' in drama_data.keys():
            is_drama = True
        else: 
            is_drama = False
       
        if is_drama:
            embed = discord.Embed(
            colour=discord.Colour.green(),
            title=drama_data['drama'],
                    description=drama_data['summary']
                )
            embed.set_author(name="Drama bot", icon_url="https://cdn.discordapp.com/attachments/625510693499568138/771565443461808128/twice-fingerheart-prints.jpg")
            embed.set_image(url=drama_data['poster'])
            embed.add_field(name="Episodes", value=drama_data['episodes'], inline=True)
            embed.add_field(name="Country", value=drama_data['country'], inline=True)
            embed.add_field(name="Score", value=drama_data['score'],inline=True)
            embed.add_field(name="Genres", value=drama_data['genres'], inline=True)
            if(drama_data['score'] == 'N/A'):
                embed.add_field(name="Airs", value=drama_data['airs'], inline=True)
            else:
                embed.add_field(name = "Aired", value = drama_data['aired'],inline=True)
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
            colour=discord.Colour.green(),
            title=drama_data['movie'],
                    description=drama_data['summary']
                )
            embed.set_author(name="Drama bot", icon_url="https://cdn.discordapp.com/attachments/625510693499568138/771565443461808128/twice-fingerheart-prints.jpg")
            embed.set_image(url=drama_data['poster'])
            embed.add_field(name="Duration", value=drama_data['duration'], inline=True)
            embed.add_field(name="Country", value=drama_data['country'], inline=True)
            embed.add_field(name="Score", value=drama_data['score'],inline=True)
            embed.add_field(name="Genres", value=drama_data['genres'], inline=True)
            embed.add_field(name="Release Date", value=drama_data['release date'], inline=True)
            await message.channel.send(embed=embed)
       
    if message.content.startswith('$trending'):
        trending_shows = trending.get_trending()
        value = ""
        i=1
        while i<11:
            value+= str(i)+". " + trending_shows[i] + '\n' + '\n'
            i+=1

        embed = discord.Embed(
            colour = discord.Colour.red(),
            title='Top 10 Trending Shows'   
        )
        embed.add_field(name="** **", value = value)
        await message.channel.send(embed=embed)
    
    if message.content.startswith('$recs '):
        parse_message = message.content.split()[1:]
        get_name = ' '.join(parse_message)
        _name = get_name.title()
        drama_link = Search.search_drama(message.content)
        rec_list = recommendations.get_recs(drama_link)
        value=''
        i=1
        while i<len(rec_list):
            value+=":small_blue_diamond:"+ rec_list[i] + '\n' + '\n'
            i+=1
        
        embed = discord.Embed(
            colour = discord.Colour.orange(),
            title='Shows Similar To '+_name            
        )
        embed.set_thumbnail(url=rec_list[0])
        embed.add_field(name="** **", value = value )
        await message.channel.send(embed=embed)      
    
    if message.content.startswith('$help'):
        embed = discord.Embed(
            colour = discord.Colour.light_gray(),
            title='List Of Commands Used By DramaBot'      
        )
        value =''
        for cmd, desc in bot_cmds.items():
            value +=('**'+cmd+'**' + ":" + desc + '\n' + '\n')
        embed.add_field(name="** **", value = value )
        await message.channel.send(embed=embed)
        

client.run(os.getenv('TOKEN'))