from PIL import ImageDraw


def line(image, start, end, color):
    draw = ImageDraw.Draw(image)
    draw.line((start, end), fill=color, width=2)


def rectangle(image, start, end, color):
    draw = ImageDraw.Draw(image)
    draw.rectangle((start, end), outline=color)
