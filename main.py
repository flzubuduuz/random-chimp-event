#1. ESENCIALES
#libraries y weas para que funcione el bot
import discord
import os
import json
import random
import asyncio
from datetime import datetime, timedelta, timezone
from dateutil import parser
from discord.ext import commands
from discord.ext.commands import has_permissions
from keep_alive import keep_alive
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='%rce ', intents=intents)
bot.remove_command('help')


#IMPORTAR .JSONS
#times
times_file = open("times.json", "r")
times = json.load(times_file)
times_file.close()

#nicks
nicks_file = open("nicks.json", "r")
nicks = json.load(nicks_file)
nicks_file.close()


#DEFICIONES
#userlist/oldnicks
userlist = {}
oldnicks = {}

#gifs
crazymonkey = random.choice([
  "https://tenor.com/view/monkey-animal-crazy-wild-animal-gif-16991056",
  "https://tenor.com/view/monkey-weird-funny-crazy-gif-20323697",
  "https://tenor.com/view/monkey-fast-spin-go-crazy-monky-gif-17655648",
  "https://tenor.com/view/gibbon-monkey-mingler-hoot-insane-gif-19328551",
  "https://tenor.com/view/and-so-it-begins-random-chip-event-monkey-gif-16455051",
  "https://tenor.com/view/ftp-police-monkey-slap-acab-gif-14097289",
  "https://tenor.com/view/what-acool-summer-animals-gif-monkey-kothi-gif-18975398",
  "https://tenor.com/view/kouga-monkey-rotate-spin-gif-16774879",
  "https://tenor.com/view/monkey-spin-orangutan-meme-gif-17118773"
])

sadmonkey = random.choice([
  "https://tenor.com/view/monkey-shock-gif-9250912",
  "https://tenor.com/view/sad-gibbon-sad-gibbon-monkey-sad-monkey-gif-19435323",
  "https://tenor.com/view/monkey-stress-mad-gif-15327798",
  "https://tenor.com/view/bus-sad-monkey-orangutan-alone-gif-12652028"
])

#embeds
help_embed=discord.Embed(title="OO OO! Aquí hay una lista de comandos disponibles:", description="_Nota: necesitas el permiso de **Gestionar roles** para que el bot responda a tus comandos._", color=0xf40101)
help_embed.add_field(name='%rce start "apodo" _tiempo_', value="Crea un nuevo evento con el apodo entre comillas, durante el tiempo especificado.\nEl tiempo tiene tres parámetros (aunque puedes utilizar solo uno o dos): **m** (minutos), **h** (horas) y **d** (días).\n_EJEMPLO:_ si quieres que el evento dure 2 días y 50 minutos, escribe **2d 50m**.\nTambién puedes escribir **0** si quieres que el evento dure indefinidamente.", inline=False)
help_embed.add_field(name="%rce stop", value="Anula el evento actual.", inline=False)
help_embed.add_field(name="%rce help", value="Muestra este mensaje de ayuda!", inline=False)
help_embed.add_field(name="**IMPORTANTE**: intenta ubicar el rol del bot lo más alto posible en la jerarquía de roles, para que así el bot pueda renombrar a la mayor cantidad de usuarios posibles.", value="\u200B", inline=False)
help_embed.add_field(name="¿Qué es este bot?", value='Gracias por preguntar! No tengo ni idea.', inline=False)
help_embed.add_field(name="\u200B", value="by flzubuduuz. [Repositorio.](https://github.com/flzubuduuz/random-chimp-event)", inline=False)

error_embed=discord.Embed(title="Hubo un error procesando tu comando 🐒", description="Utiliza **%rce help** para revisar si tu comando y los parámetros están bien escritos, o si tienes los permisos necesarios para ejecutar ese comando.", color=0xf40101)

#start
async def start(ctx, newnick, duration):

  serverid = str(ctx.guild.id)

  await ctx.send(crazymonkey)

  userlist[serverid] = {}
  userlist[serverid]["channelid"] = ctx.channel.id

  if not serverid in times:
    
    for user in ctx.guild.members:
      userlist[serverid][str(user.id)] = user.nick
    
    userlist_file = open(serverid + ".json", "w")
    json.dump(userlist[serverid], userlist_file)
    userlist_file.close()

  unable = ""
  for user in ctx.guild.members:
    try: await user.edit(nick=newnick)
    except:
        unable += ("\n" + user.mention)
  if not unable == "":
    unable = "\n\nNo se pudieron cambiar los apodos de los siguientes usuarios:\n" + unable

  if not duration == 0:
    times[serverid] = str(datetime.now(timezone.utc) + timedelta(minutes=eval(duration)))
  nicks[serverid] = newnick

  times_file = open("times.json", "w")
  json.dump(times, times_file)
  times_file.close()

  nicks_file = open("nicks.json", "w")
  json.dump(nicks, nicks_file)
  nicks_file.close()

  del userlist[serverid]

  await ctx.send("**RANDOM CHIMP EVENT IS READY**" + unable)

#stop
async def stop(ctx, serverid: str):

  oldnicks_file = open(serverid + ".json", "r")
  oldnicks[serverid] = json.load(oldnicks_file)
  oldnicks_file.close()

  if ctx == discord.ext.commands.Context:
    ctx.guild = bot.get_guild(int(serverid))
    ctx.send = ctx.guild.get_channel(oldnicks[serverid]["channelid"]).send

  await ctx.send(sadmonkey)

  if serverid in times:
    del times[serverid]
  del nicks[serverid]

  unable = ""
  for user in ctx.guild.members:
    try: 
      if str(user.id) in oldnicks[serverid]:
        await user.edit(nick = oldnicks[serverid][str(user.id)])
      else: await user.edit(nick = None)
    except:
      unable += ("\n" + user.mention)
  if not unable == "":
    unable = "\n\nNo se pudieron cambiar los apodos de los siguientes usuarios:\n" + unable

  os.remove(serverid + ".json")

  times_file = open("times.json", "w")
  json.dump(times, times_file)
  times_file.close()

  nicks_file = open("nicks.json", "w")
  json.dump(nicks, nicks_file)
  nicks_file.close()

  await ctx.send("**RANDOM CHIMP EVENT IS OVER**" + unable)

  del oldnicks[serverid]
  del ctx.guild
  del ctx.send


#INICIO
@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game(name="con el hado del mundo | %rce help"))
  print('{0.user} is up and running'.format(bot))
  await timecheck()


#COMANDOS
#start
@bot.command(name="start")
@has_permissions(manage_nicknames=True)
async def requeststart(ctx, newnick: str, *, duration):

  #longnick embed
  longnick_embed = discord.Embed(title="El apodo que escogiste es muy largo 🐒", description="Debe ser de 32 caracteres o menos, el tuyo tenía **" + str(len(newnick)) + "** caracteres.", color=0xf40101)

  #nick extenso
  if len(newnick) > 32:
    await ctx.send(embed = longnick_embed)
    return

  #convert time
  duration = duration.replace("m", "*1").replace("h", "*60").replace("d", "*1440").replace(" ", "+")

  days = divmod(eval(duration), 1440)
  hours = divmod(days[1], 60)
  minutes = hours[1]
  niceduration = str(days[0]) + " días, " + str(hours[0]) + " horas y " + str(minutes) + " minutos"

  #embed
  sure_embed=discord.Embed(title="Estás apunto de iniciar un evento...", color=0xff0000)
  sure_embed.add_field(name="\u200B", value="El nuevo apodo será **" + newnick + "** y el evento durará **" + niceduration + "**.\n\n**¿Estás seguro?** Reacciona con 🐵 para activar el evento.\n_El evento se cancelará si no hay una reacción durante los próximos 30 segundos._", inline=False)

  #send embed
  await ctx.send(embed=sure_embed)

  def check(reaction, user):
    return user == ctx.message.author and str(reaction.emoji) == '🐵'

  try:
    reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
  except asyncio.TimeoutError:
    await ctx.send(":stopwatch: **Se acabó el tiempo de espera y se canceló el evento.**")
  else:
    await start(ctx, newnick, duration)

#stop
@bot.command(name="stop")
@has_permissions(manage_nicknames=True)
async def stoprequest(ctx):

  if not str(ctx.guild.id) in times:
    await ctx.send("🐵 **No hay ningún evento actualmente, por lo que no se puede anular nada.** 🐵")
    return

  await ctx.send(":no_entry_sign: **Estás a punto de anular el evento actual**. Reacciona con 🐵 para proseguir. \n_El evento continuará si no hay una reacción durante los próximos 30 segundos._")

  def check(reaction, user):
    return user == ctx.message.author and str(reaction.emoji) == '🐵'

  try:
    reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
  except asyncio.TimeoutError:
    await ctx.send(":stopwatch: **Se acabó el tiempo de espera, por lo que el evento continuará.")
  else:
    await stop(ctx, str(ctx.guild.id))

#help
@bot.command()
async def help(ctx):
  await ctx.send(embed=help_embed)

#error
@bot.event
async def on_command_error(ctx, error):
  print(error)
  await ctx.send(embed=error_embed)


#TIMEOUT
async def timecheck():
  while True:
    try:
      for i in times:
        if datetime.now(timezone.utc) > parser.parse(times[i]):
          await stop(discord.ext.commands.Context, i)
      await asyncio.sleep(10)
    except: return


#DURING EVENT
@bot.event
async def on_member_join(member):
  try: await member.edit(nick=nicks[str(member.guild.id)])
  except: return

@bot.event
async def on_member_update(before, member):
  serverid = str(member.guild.id)

  if serverid in times and not serverid in oldnicks and not serverid in userlist:
    try: await member.edit(nick=nicks[serverid])
    except: return


#FIN
#pingea al bot
keep_alive()

#token
bot.run(os.environ['TOKEN'])