from datetime import date
from tgtg import TgtgClient
import json
import os
import discord
import time
    
users = []
discord_client:discord.Client = None

def init():
    global users, discord_client
    f = open('config.json')
    u = json.load(f)
    users = u['users']
    #Puis on run le bot
    token = u['bot_token']    
    intents = discord.Intents.default()
    intents.message_content = True
    discord_client = discord.Client(intents=intents)

    @discord_client.event
    async def on_ready():
        print("Bot ready")
        await retrieve()

    discord_client.run(token)

async def retrieve():
    while True:
        print('Fetching for all users at date', date.today().strftime('%d/%m - %H:%M:%S'))
        for uindex, user in enumerate(users):
            client = TgtgClient(access_token=user['access_token'], refresh_token=user['refresh_token'], user_id=user['user_id'])
            items = client.get_items(with_stock_only=True)
            fileName = f'users_data/{uindex}.json'
            if os.path.exists(fileName):
                data = json.load(open(fileName))['orders']
            else:
                data = []
            ndata = []
            for item in items:
                end = item['purchase_end']
                available = item['items_available']
                i = item['item']
                price = i['price_including_taxes']['minor_units'] / 100
                desc = i['description']
                name = i['name']
                id = i['item_id']
                store = item['store']['store_name']
                print(name, desc, price, id, store, available, end)
                ndata.append({'name':name, 'desc':desc, 'price':price, 'id':id, 'store':store,'available':available, 'end': end})
                if len(list(filter(lambda a : a['id']==ndata['id'], data))) == 0:
                    print("I am sending a msg...")
                    discord_id = user['discord_id']
                    embed = discord.Embed(title="Un nouvel item est apparu !", description=f"{name}\n{desc}", color=discord.Color.blue())
                    discord_user = await discord_client.fetch_user(discord_id)
                    await discord_user.send(embed=embed)

            f = open(fileName, 'w')
            json.dump({"orders": ndata}, f)
        print("End of fetching, everything's okay")
        time.sleep(60 * 15)
                

if __name__=="__main__":
    init()






