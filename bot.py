from discord import channel
import requests
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import time
import os


price_url = 'https://api.coingecko.com/api/v3/simple/price?ids=basic-attention-token&vs_currencies=USD'
gas_url = 'https://www.gasnow.org/api/v3/gas/price'

def bat_current_price(url):
    r = requests.get(url)
    bat_json = r.json()['basic-attention-token']
    return float(round((bat_json['usd']),3))

def gas_current_value(url):
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()['data']
        return (int(data['standard']//1e9))
    else:
        print("Error")

bot = commands.Bot(command_prefix='$')
@bot.command()
@has_permissions(manage_channels=True)
async def config(ctx, arg):
    cat = discord.utils.get(ctx.guild.categories, name="📈💲 BAT | Gas Tracker 💲 📈")
    if(cat):
        await ctx.send("Category already exists! Type $start tracker")
    else:
        await ctx.guild.create_category("📈💲 BAT | Gas Tracker 💲 📈")
        cat = discord.utils.get(ctx.guild.categories, name="📈💲 BAT | Gas Tracker 💲 📈")
        await ctx.send("Category create!")
        guild = ctx.message.guild
        channel_name_updated = "USD | Gwei"
        await guild.create_voice_channel(name=channel_name_updated, category=cat)

        await ctx.send("Channels ready to track. Type $start tracker")


@bot.command(price_url=price_url, gas_url=gas_url)
@has_permissions(manage_channels=True)

async def start(ctx, arg):
    cat = discord.utils.get(ctx.guild.categories, name="📈💲 BAT | Gas Tracker 💲 📈")
    list_voice_ch = cat.channels
    starttime = time.time()
    while True:
        bat_price = bat_current_price(price_url)
        gas_value = gas_current_value(gas_url)
        channel_name_updated = str(bat_price) + " USD " + " | " + str(gas_value) + " Gwei"
        # await ctx.send(channel_name_updated)
        print(channel_name_updated)
        ch = discord.utils.get(ctx.guild.channels, id=list_voice_ch[0].id)
        await ch.edit(name = channel_name_updated)
        time.sleep(360.0 - ((time.time() - starttime) % 360.0))


if __name__ == '__main__':
    print("Running")
    bot.run(os.environ.get('TOKEN'))
    