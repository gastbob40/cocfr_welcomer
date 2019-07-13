def write_text(image, x, y, text, font):
    for i in range(1, 3):
        image.text((x - i, y - i), text, font=font, fill="black")
        image.text((x + i, y - i), text, font=font, fill="black")
        image.text((x - i, y + i), text, font=font, fill="black")
        image.text((x + i, y + i), text, font=font, fill="black")
    image.text((x, y), text, (255, 255, 255), font=font)
    return image
