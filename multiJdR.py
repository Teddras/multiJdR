import os
import discord
import autorisation

from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix="%")

token = autorisation.token

@client.event
#détection de l'allumage du bot
async def on_ready():
    await client.change_presence(status=discord.Status.online,activity=discord.Game("jeu de rôle"))



@client.command()
async def pause(ctx):
    print(str(ctx))
    await ctx.send("une pause est demandée")
    membres = ctx.guild.members
    print(membres)
    print(ctx.author.voice)
    print("{} est dans le salon vocal {}".format(ctx.author.name,ctx.author.voice.channel.name))
    await ctx.send("{} est dans le salon vocal {}".format(ctx.author.name,ctx.author.voice.channel.name)) 
    #si pas connecté None comme voice





print("Lancement du bot jdr...")
client.run(token)