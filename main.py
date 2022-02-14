import requests
from bs4 import BeautifulSoup
import discord
import asyncio
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

targets = {
    '993_MENS': [
        'https://www.newbalance.com/pd/made-in-usa-993/MR993V1-M.html#dwvar_MR993V1-10103_style=MR993GL&dwvar_MR993V1-10103_width=D&mpspid=MR993V1-M&pid=MR993V1-10103&quantity=1',
        '9',
        "993 Men's Standard"
    ],
    '993_WOMENS': [
        'https://www.newbalance.com/pd/made-in-usa-993/WR993V1-MPS.html#dwvar_WR993V1-2382_style=WR993GL&dwvar_WR993V1-2382_width=B&mpspid=WR993V1-MPS&pid=WR993V1-2382&quantity=1',
        '10',
        "993 Women's Standard"
    ],
}


def checkStock(url, size, name):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        target_btn = soup.select_one(f'button[aria-describedby="{size}"]')
        if 'selectable' in target_btn['class']:
            # IN STOCK ACTION
            print(f'{name} size {size} IN STOCK!')
            return True
        else:
            # NOT IN STOCK ACTION
            print(f'{name} size {size} not in stock...')
            return False
    else:
        print('URL ERROR')
        return False


client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


async def background_task():
    await client.wait_until_ready()
    channel = client.get_channel(int(CHANNEL_ID))
    while not client.is_closed():
        for key in targets:
            is_in_stock = checkStock(targets[key][0], targets[key][1], targets[key][2])
            if is_in_stock:
                await channel.send(f'{targets[key][2]} size {targets[key][1]} IN STOCK!')
        await asyncio.sleep(20)

client.loop.create_task(background_task())
client.run(TOKEN)
