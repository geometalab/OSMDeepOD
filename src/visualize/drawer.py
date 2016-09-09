from PIL import ImageDraw


def line(image, start, end, color):
    draw = ImageDraw.Draw(image)
    draw.line((start, end), fill=color, width=2)


def rectangle(image, start, end, color):
    draw = ImageDraw.Draw(image)
    draw.rectangle((start, end), outline=color)


def point(image, position, color):
    draw = ImageDraw.Draw(image)
    x, y = position
    circle = [(x - 3, y - 3), (x + 3, y + 3)]
    draw.ellipse(circle, fill=color, outline=color)
