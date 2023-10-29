import os
import cv2
import discord
import numpy as np
from time import sleep
from discord import Embed
from discord.ext import commands
from datetime import datetime

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
        threshold = 0.5
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
    embed.set_image(url="attachment://./test/image.png")
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
        embed2.set_image(url="attachment://preview/"+Name)
        embed2.set_thumbnail(url="attachment://src/"+Name)
        embed2.timestamp = datetime.utcnow()
    else :
        embed2 = Embed(
            title = "Fail",
            description = "Cannot Identify Image",
            colour = 0xe74c3c
        )
        embed2.timestamp = datetime.utcnow()
      
    await old_embed.edit(embed=embed2)



bot.run("MTE2Nzg3NTEyOTQ3NzQ0Nzg2Mg.GHfQJQ.IcgjOfSu0qaYS6OtKcs7aHBzHB2f3BgaUo2JzE")
