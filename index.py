import json
from datetime import datetime, timedelta

import discord

from images_creator.index import get_image

client = discord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user} in {len(client.guilds)} guilds')


@client.event
async def on_message(message):
    if message.author == client.user:
        return


@client.event
async def on_member_join(member: discord.Member):
    # A lot of checks
    with open('config.json', "r") as file:
        data = json.load(file)

    # Check if the user is a banned user
    if member.display_name in data['banned_users']:
        return

    # Check if the user has joined the server during last 30 seconds
    now = datetime.now()
    if member.display_name == data['last_user']['username']:
        last_time = datetime.strptime(data['last_user']['date'], '%Y-%m-%d %H:%M:%S.%f')

        if now - last_time < timedelta(seconds=30):
            data['banned_users'].append(member.display_name)
            await client.get_channel(377179445640822784).send('RAID EN COURS')
            with open("config.json", "w") as file:
                json.dump(data, file)
            return

    data['last_user']['username'] = member.display_name
    data['last_user']['date'] = now.strftime('%Y-%m-%d %H:%M:%S.%f')

    with open("config.json", "w") as file:
        json.dump(data, file)

    # Create image and text
    avatar_url = None
    if not member.avatar:
        avatar_url = 'https://external-preview.redd.it/9HZBYcvaOEnh4tOp5EqgcCr_vKH7cjFJwkvw-45Dfjs.png?width=561&auto=webp&s=b66485d47a4cb60774d5905df9044583af568eb4'
    else:
        avatar_url = f'https://cdn.discordapp.com/avatars/{member.id}/{member.avatar}'

    fp = get_image(member.display_name, avatar_url, len(member.guild.members))

    content = f"<@{member.id}>, Bienvenue sur **Clash of Clans Français** <:COCFR:362270336437452800>\n\n" \
        f"Afin de te familiariser avec le serveur tu n'as pas accès à tous les salons. Tu pourras faire de la pub ou du recrutement une fois que tu auras atteint le **level 5**<:barbar:408701460209991715> (Barbare)\n" \
        f"Ce niveau est très rapide à atteindre <:Sortdevitesse:349829871859662848>\n\n" \
        f"Pour plus d'infos tape **level** dans <#289476916044627978> et pense à lire les <#280735672527224842>."

    await client.get_channel(278653494846685186).send(content=content, file=discord.File(fp=fp, filename="my_file.png"))


with open('config.json') as f:
    token = json.load(f)['token']
client.run(token)

# get_image('https://cdn.discordapp.com/avatars/330361902997962752/1e17bc7e6eec3258eed0a71c7cdd833b?size=256')
