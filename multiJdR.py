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

#lien d'invitation : 
class Chrono():
    def __init__(self,temps = 0):
        self.tempsEcoule = temps
        self.tempsRef = 0
        self.pause = True 
    def lancement(self):
        while True:
            if not self.pause:
                temps = time.time()
                self.tempsEcoule += self.tempsRef - temps
                self.tempsRef = temps
                print(self.tempsEcoule)

class MonRobot(commands.Bot):
    def __init__(self,command_prefix = "!"):
        commands.Bot.__init__(self,command_prefix = command_prefix)
        self.chronos = {}
        self.canaux = {}
    async def cloches(self,serveur,coups):
        try:
            for canal in self.canaux[serveur]:
                voc = await canal.connect()
                i =0
                while i < coups:
                    print("cloche {}".format(i))
                    await voc.play(discord.FFmpegOpusAudio("clocheTest.mp3"))
                    while voc.isplaying():
                        time.sleep(0.1)
                    i += 1
                voc.disconnect()
        except ClientException:
            voc.disconnect()
            

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
async def chrono(ctx):
    serveur = str(ctx.guild.id)
    if serveur in client.chronos.keys():
        pass

@client.command()
async def cloches(ctx,nombre):
    serveur = str(ctx.guild.id)
    try:
        coups = int(nombre)
        if serveur in client.canaux.keys():
            if client.canaux[serveur] != []:
                await client.cloches(serveur,coups)
            else:
                ctx.send("pas de canaux enregistré")
        else:
            ctx.send("pas de canaux enregistré")
    except ValueError:
        print("erreur de valeur")


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
