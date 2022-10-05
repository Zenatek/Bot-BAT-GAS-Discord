from discord import channel
import requests
import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
import time
import os
import asyncio
from datetime import datetime




price_url = 'https://api.coingecko.com/api/v3/simple/price?ids=basic-attention-token&vs_currencies=USD'
#gas_url = 'https://www.etherchain.org/api/gasPriceOracle'
gas_url = 'https://ethgasstation.info/api/ethgasAPI.json?api-key=' + os.environ.get('APIKEY')
h24_url = 'https://api.coingecko.com/api/v3/coins/basic-attention-token?localization=false&tickers=false&community_data=false&developer_data=false&sparkline=false'

def bat_current_price(url):
    r = requests.get(url)
    bat_json = r.json()['basic-attention-token']
    return float(round((bat_json['usd']),3))

def gas_current_value(url):
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        return (int(data['average'])//10)
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

# @bot.command()
# @has_permissions(manage_channels=True)
# async def config(ctx, arg):
#     cat = discord.utils.get(ctx.guild.categories, name="📈💲 BAT | Gas Tracker 💲 📈")
#     if(cat):
#         await ctx.send("Category already exists! Type $start tracker")
#     else:
#         await ctx.guild.create_category("📈💲 BAT | Gas Tracker 💲 📈")
#         cat = discord.utils.get(ctx.guild.categories, name="📈💲 BAT | Gas Tracker 💲 📈")
#         await ctx.send("Category create!")
#         guild = ctx.message.guild
#         channel_name_updated = "USD | Gwei"
#         await guild.create_voice_channel(name=channel_name_updated, category=cat)
#         channel_name_updated = "24h: "
#         await guild.create_voice_channel(name=channel_name_updated, category=cat)

#         await ctx.send("Channels ready to track. Type &start tracker")


# @bot.command(price_url=price_url, gas_url=gas_url, h24_url=h24_url)
# @has_permissions(manage_channels=True)

# async def channel_track(ctx, arg):
#     cat = discord.utils.get(ctx.guild.categories, name="📈💲 BAT | Gas Tracker 💲 📈")
#     list_voice_ch = cat.channels
#     starttime = time.time()
    
#     while True:
#         try:
#            bat_price = bat_current_price(price_url)
#            gas_value = gas_current_value(gas_url)
#            #gas_value = 0
#            h24_perc_value = h24_value(h24_url)

#            # UPDATE PRICE AND GAS
#            channel_name_updated = str(bat_price) + " USD " + " | " + str(gas_value) + " Gwei"
#         #    await ctx.send(channel_name_updated)

#            ch = discord.utils.get(ctx.guild.channels, id=list_voice_ch[0].id)
#            await ch.edit(name = channel_name_updated)

#            # UPDATE 24h PERCENT
#            if h24_perc_value >= 0:
#                channel_name_updated = ('24h: ↗️  ' + str(h24_perc_value) + '%')
#            else:
#                channel_name_updated = ('24h: ↘️  ' + str(h24_perc_value) + '%')
#            print(channel_name_updated)
           
#            ch = discord.utils.get(ctx.guild.channels, id=list_voice_ch[1].id)
#            await ch.edit(name = channel_name_updated)

#            time.sleep(3600)
#         except:
#            pass



async def set_presence(percent):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=percent))


# @tasks.loop(seconds=60)
async def rename(ctx, arg):
    # try:
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)

            bat_price = bat_current_price(price_url)
            gas_value = gas_current_value(gas_url)
            h24_perc_value = h24_value(h24_url)

            # UPDATE PRICE AND GAS
            channel_name_updated = str(bat_price) + " $ " + " | " + str(gas_value) + " Gwei"
            print(channel_name_updated)
            await bot.user.edit(username=channel_name_updated)
            user = ctx.guild.me
            await user.edit(nick=channel_name_updated)      

            # UPDATE 24h PERCENT
            if h24_perc_value >= 0:
                percent = ('24h: ↗️  ' + str(h24_perc_value) + '%')
            else:
                percent = ('24h: ↘️  ' + str(h24_perc_value) + '%')

            await set_presence(percent)
            print(percent)

            await asyncio.sleep(3600)

    # except :
    #     pass
@bot.command(price_url=price_url, gas_url=gas_url, h24_url=h24_url)
async def bot_track(ctx,arg):
    await rename(ctx,arg)

if __name__ == '__main__':
    print("Running")
    bot.run(os.environ.get('TOKEN'))
    
