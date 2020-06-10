import os
import discord
import ffmpeg
from discord import ClientException
import autorisation
import nacl
import time
import threading
from discord.ext import commands
from discord.utils import get

#lien d'invitation : https://discord.com/api/oauth2/authorize?client_id=716174723494576230&permissions=0&scope=bot
class Chrono():
    def __init__(self,temps = 0):
        self.tempsEcoule = temps
        self.tempsRef = 0
        self.pause = True 
    def lancement(self):
        while True:
            if not self.pause:
                temps = time.time()
                self.tempsEcoule += temps - self.tempsRef
                self.tempsRef = temps
                # print(self.tempsEcoule)

class MonRobot(commands.Bot):
    def __init__(self,command_prefix = "!"):
        commands.Bot.__init__(self,command_prefix = command_prefix)
        self.chronos = {}
        self.canaux = {}
        self.threads = {}
    async def cloches(self,serveur,coups):
        try:
            for canal in self.canaux[serveur]:
                voc = await canal.connect()
                i =0
                while i < coups:
                    print("cloche {}".format(i))
                    await voc.play(discord.FFmpegOpusAudio("clocheTest.mp3"))
                    time.sleep(1.3)
                    i += 1
                voc.disconnect()
        except ClientException:
            voc.disconnect()

def secTohms(nb_sec):
    q,s=divmod(nb_sec,60)
    h,m=divmod(q,60)
    return (h,m,s)

client = MonRobot("%")

@client.command()
async def ajouterCanal(ctx):
    serveur = str(ctx.guild.id)
    print(serveur)
    if not serveur in client.canaux.keys():
        client.canaux[serveur] = []
    if not ctx.author.voice == None:
        if not ctx.author.voice.channel in client.canaux[serveur]:
            print(ctx.author.voice) 
            client.canaux[serveur].append(ctx.author.voice.channel)
        else:
            print("canal déjà enregistré")
    else:
        print("pas de serveur vocal détecter pour {}".format(ctx.author))
    print(client.canaux)

@client.command()
async def startChrono(ctx):
    serveur = str(ctx.guild.id)
    if serveur in client.chronos.keys():
        if not serveur in client.threads.keys():
            client.threads[serveur] = threading.Thread(target= client.chronos[serveur].lancement)
            client.threads[serveur].start()
        else:
            await ctx.send("chrono déjà lancé")
    else:
        await ctx.send("chrono inexistant")
    print(client.threads)

@client.command()
async def setTime(ctx,secondes):
    serveur = str(ctx.guild.id)
    try:
        secondes = int(secondes)
        if serveur in client.chronos.keys():
            client.chronos[serveur].tempsEcoule = secondes
        else:
            await ctx.send("chrono inexistant")
    except ValueError:
        await ctx.send("Vous n'avez pas rentré un nombre de secondes")

@client.command()
async def heure(ctx):
    serveur = str(ctx.guild.id)
    if serveur in client.chronos.keys():
        h,m,s = secTohms(int(client.chronos[serveur].tempsEcoule*3))
        await ctx.send("il est {}h{}m{}s".format(h,m,s))
    else:
        await ctx.send("Ce serveur n'a pas de chrono actuellement")



@client.command()
async def chrono(ctx):
    serveur = str(ctx.guild.id)
    if not serveur in client.chronos.keys():
        client.chronos[serveur] = Chrono()
    else:
        print("chrono déjà existant")
    print(client.chronos)

# @client.command()
# async def cloches(ctx,nombre):
#     serveur = str(ctx.guild.id)
#     try:
#         coups = int(nombre)
#         if serveur in client.canaux.keys():
#             if client.canaux[serveur] != []:
#                 await client.cloches(serveur,coups)
#             else:
#                 await ctx.send("pas de canaux enregistré")
#         else:
#             await ctx.send("pas de canaux enregistré")
#     except ValueError:
#         print("erreur de valeur")

@client.command()
async def pause(ctx):
    serveur = str(ctx.guild.id)
    if serveur in client.chronos.keys():
        if client.chronos[serveur].pause:
            client.chronos[serveur].tempsRef = time.time()
            client.chronos[serveur].pause = False
        else:
            client.chronos[serveur].tempsRef = time.time()
            client.chronos[serveur].pause = True
    else:
        ctx.send("Ce serveur n'a pas de chrono actuellement")

@client.event
#détection de l'allumage du bot
async def on_ready():
    await client.change_presence(status=discord.Status.online,activity=discord.Game("jeu de rôle"))

def main():
    token = autorisation.token
    print("Lancement du bot jdr...")
    client.run(token)


if __name__ == "__main__":
    main()
