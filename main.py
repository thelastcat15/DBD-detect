import os
import cv2
import discord
import numpy as np
from time import sleep
from discord import Embed
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

url = "https://raw.githubusercontent.com/thelastcat15/DBD-detect/main"

images = os.listdir("src")

intents = discord.Intents.default()
intents.message_content = True

PREFIX = '!'

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name}')


def is_image_in_image(template_path, uploaded_image):
    # Load the template and the uploaded image
    img1 = cv2.imread(template_path)
    img2 = cv2.imdecode(np.frombuffer(uploaded_image, np.uint8), cv2.IMREAD_COLOR)

    try :
        result = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
        threshold = 0.4
        locations = np.where(result >= threshold)

        return len(locations[0]) > 0
    except Exception as err :
        print(err)
        return False


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  if message.channel.id == 1167875055447978066 and len(message.attachments) == 1:
    embed = Embed(title = "Loading...", description = "", colour = 0xe67e22)
    embed.set_image(url=f"{url}/load.gif")
    embed.timestamp = datetime.utcnow()
    old_embed = await message.channel.send(embed=embed)
    
    Name = False
    for img in images:
        image_bytes = await message.attachments[0].read()
        if is_image_in_image("src/"+img, image_bytes):
            Name = img
            break

    if Name :
        embed2 = Embed(
            title = "Success",
            description = "Map Name : "+Name.replace(".png", ""),
            colour = 0x2ecc71
        )
        embed2.set_image(url=f"{url}/preview/{Name}")
        embed2.set_thumbnail(url=f"{url}/src/{Name}")
        embed2.timestamp = datetime.utcnow()
    else :
        embed2 = Embed(
            title = "Fail",
            description = "Cannot Identify Image",
            colour = 0xe74c3c
        )
        embed2.timestamp = datetime.utcnow()
      
    await old_embed.edit(embed=embed2)


bot.run(os.getenv('TOKEN'))
