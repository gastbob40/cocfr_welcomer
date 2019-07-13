import io
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageOps, ImageFont

from images_creator.writter import write_text


def get_image(username: str, image_url: str, number:int):
    image = Image.new("RGB", (1000, 322))
    background = Image.open("backgrounds/banner.jpg")  # 25x25

    size_logo = (250, 250)
    response = requests.get(image_url)
    user_logo = Image.open(BytesIO(response.content))
    user_logo = user_logo.resize(size_logo, Image.ANTIALIAS)

    # Crop the original logo (to get round image)
    mask = Image.new("L", size_logo, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size_logo, fill=255)
    user_logo_cropped = ImageOps.fit(user_logo, mask.size, centering=(0.5, 0.5))
    user_logo_cropped.putalpha(mask)

    # Paste background and user logo

    image.paste(background)
    image.paste(user_logo_cropped, (30, 40), mask)

    # Write on image
    text_written = ImageDraw.Draw(image)
    font = ImageFont.truetype("fonts/sans-serif.otf", 50)
    # font = ImageFont.truetype("fonts/coc.ttf", 40)

    write_text(text_written, 300, 90, f"{username}", font)
    write_text(text_written, 300, 150, "Bienvenue sur COC Français", font)
    write_text(text_written, 300, 210, f"Tu es le {number} èmes clasheur", font)

    fp = io.BytesIO()
    image.save(fp=fp, format="jpeg")
    fp.seek(0)

    return fp
