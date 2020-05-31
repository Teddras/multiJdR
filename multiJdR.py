import os
import discord
import autorisation
import nacl
import json
import time
from discord.ext import commands
from discord.utils import get
import ffmpeg
import texttomp3

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
vocals = []

@client.event
#détection de l'allumage du bot
async def on_ready():
    await client.change_presence(status=discord.Status.online,activity=discord.Game("jeu de rôle"))

@client.command()

@client.command()
async def voirTable(ctx):
    ctx.send(tables[str(ctx.guild.id)])

@client.command()
async def tableMJ(ctx,nomTable,*mj):
    serveur = str(ctx.guild.id)
    if not serveur in tables.keys():
        tables[serveur] = {nomTable:[]}
    for meneur in mj:
        if not meneur in tables[serveur][nomTable]:
            tables[serveur][nomTable].append(meneur)
    print("tentative d'inscription de la table dans le fichier de sauvegarde")
    with open(tablepath,"w") as f:
        json.dump(tables,f,indent=4)
        print("sauvegarde réussie")
    print(tables)



@client.command()
async def pause(ctx):
    print(str(ctx))
    await ctx.send("une pause est demandée")
    membres = ctx.guild.members
    print(membres)
    vocals = []
    if (ctx.author.voice != None):
        # test = None
        channelVocal = ctx.author.voice.channel
        print("{} est dans le salon vocal {}".format(ctx.author.name,ctx.author.voice.channel.name))
        await ctx.send("{} est dans le salon vocal {}".format(ctx.author.name,ctx.author.voice.channel.name))
        vocals.append(await channelVocal.connect())
        # test = client.voice_clients
        for truc in vocals:
            truc.play(discord.FFmpegPCMAudio("test.mp3"), after=lambda e: print('done', e))
            time.sleep(10)
            await truc.disconnect()
    else:
        await ctx.send("{} n'est pas connecté".format(ctx.author.name))


print("Lancement du bot jdr...")
client.run(token)