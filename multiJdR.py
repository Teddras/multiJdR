import os
import discord
import autorisation
import nacl
import json
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix="%")

token = autorisation.token
tablepath = autorisation.tables
tables = {}
#fonction de chargement des tables depuis fichier json
if os.path.isfile(tablepath):
    with open(tablepath,"r") as f:
        tables = json.load(f)
with open(tablepath,"w") as f:
    json.dump(tables,f,indent=4)

@client.event
#détection de l'allumage du bot
async def on_ready():
    await client.change_presence(status=discord.Status.online,activity=discord.Game("jeu de rôle"))

@client.command()
async def tableMJ(ctx,nomTable,mj):
    pass



@client.command()
async def pause(ctx):
    print(str(ctx))
    await ctx.send("une pause est demandée")
    membres = ctx.guild.members
    print(membres)
    
    #print(ctx.author.voice)
    #si pas connecté None comme voice
    if (ctx.author.voice != None):
        test = None
        channelVocal = ctx.author.voice.channel
        print("{} est dans le salon vocal {}".format(ctx.author.name,ctx.author.voice.channel.name))
        await ctx.send("{} est dans le salon vocal {}".format(ctx.author.name,ctx.author.voice.channel.name))
        await channelVocal.connect()
        test = client.voice_clients
        for truc in test:
            print(truc.channel)
            await truc.disconnect()

    else:
        await ctx.send("{} n'est pas connecté".format(ctx.author.name))






print("Lancement du bot jdr...")
client.run(token)