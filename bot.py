from discord import channel
import requests
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import time
import os


price_url = 'https://api.coingecko.com/api/v3/simple/price?ids=basic-attention-token&vs_currencies=USD'
gas_url = 'https://www.etherchain.org/api/gasPriceOracle'
h24_url = 'https://api.coingecko.com/api/v3/coins/basic-attention-token?localization=false&tickers=false&community_data=false&developer_data=false&sparkline=false'

def bat_current_price(url):
    r = requests.get(url)
    bat_json = r.json()['basic-attention-token']
    return float(round((bat_json['usd']),3))

def gas_current_value(url):
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        return (int(data['currentBaseFee']))
    else:
        print("Error")

def h24_value(url):
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()['market_data']['price_change_percentage_24h']
        return (float(round(data,2)))
    else:
        print("Error")

bot = commands.Bot(command_prefix='&')
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
        channel_name_updated = "24h: "
        await guild.create_voice_channel(name=channel_name_updated, category=cat)

        await ctx.send("Channels ready to track. Type &start tracker")


@bot.command(price_url=price_url, gas_url=gas_url, h24_url=h24_url)
@has_permissions(manage_channels=True)

async def start(ctx, arg):
    cat = discord.utils.get(ctx.guild.categories, name="📈💲 BAT | Gas Tracker 💲 📈")
    list_voice_ch = cat.channels
    starttime = time.time()
    while True:
        bat_price = bat_current_price(price_url)
        gas_value = gas_current_value(gas_url)
        h24_perc_value = h24_value(h24_url)

        # UPDATE PRICE AND GAS
        channel_name_updated = str(bat_price) + " USD " + " | " + str(gas_value) + " Gwei"
        # await ctx.send(channel_name_updated)
        print(channel_name_updated)
        ch = discord.utils.get(ctx.guild.channels, id=list_voice_ch[0].id)
        await ch.edit(name = channel_name_updated)

        # UPDATE 24h PERCENT
        if h24_perc_value >= 0:
            channel_name_updated = ('24h: ↗️  ' + str(h24_perc_value) + '%')
        else:
            channel_name_updated = ('24h: ↘️  ' + str(h24_perc_value) + '%')
        print(channel_name_updated)
        ch = discord.utils.get(ctx.guild.channels, id=list_voice_ch[1].id)
        await ch.edit(name = channel_name_updated)

        time.sleep(360.0 - ((time.time() - starttime) % 360.0))


if __name__ == '__main__':
    print("Running")
    bot.run(os.environ.get('TOKEN'))
