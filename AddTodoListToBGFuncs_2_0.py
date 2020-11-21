import ctypes
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# ------------------- consts ------------------- #
COMPLETE = 'c'
TODO = 't'

BLANK_BG = "resources\\bg_blank.jpg"
OUTPUT_BG = "resources\\bg.jpg"
TODO_LIST = "resources\\list.txt"

FONT = "arial.ttf"
FONT_SIZE = 60
LOCATION = (2450, 690)

IMAGE = Image.open(os.path.join(sys.path[0], BLANK_BG))


# ------------------- funcs ------------------- #
def read_txt_from_list():
    with open(TODO_LIST) as f:
        lst = []
        for line in f.read().split('\n'):
            lst.append(line.rsplit(',', 1))
        # print(lst)
        return lst


def update_list(txt):
    with open(TODO_LIST, 'w') as f:
        for line in txt:
            f.write(line)


def draw_txt(pos):
    image = Image.open(os.path.join(sys.path[0], BLANK_BG))  # open img
    draw = ImageDraw.Draw(image)  # create draw object
    font = ImageFont.truetype(FONT, size=FONT_SIZE)
    # print(image.size)
    location = list(pos)
    space = 90

    txt = read_txt_from_list()
    for line in txt:
        draw.text(tuple(location), line[0], font=font)
        if line[1] == COMPLETE and line[0] != '':
            text_width, text_height = draw.textsize(line[0], font=font)
            draw.line([location[0] - 5, location[1] + text_height / 2,
                       location[0] + text_width + 5, location[1] + text_height / 2],
                      width=5)

        location[1] += space

    image.save(os.path.join(sys.path[0], OUTPUT_BG))


def set_bg():
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(sys.path[0], OUTPUT_BG), 1)
