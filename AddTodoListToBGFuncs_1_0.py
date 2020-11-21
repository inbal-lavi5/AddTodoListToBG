import ctypes
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# ------------------- consts ------------------- #
COMPLETE = 'c'
ADD = 'a'
QUIT = 'q'
INVALID_MSG = "invalid input"
INSTRUCTIONS = "# WELCOME #\n" \
               f"    {COMPLETE} - to complete tasks (delete them)\n" \
               f"    {ADD} - to add tasks\n" \
               f"    {QUIT} - to exit\n"

DELETE_USAGE = "lines to delete: <line> <line> ...\n"
ADD_USAGE = "add clause: <line> <message>\n"

BLANK_BG = "resources\\bg_blank.jpg"
OUTPUT_BG = "resources\\bg.jpg"
TODO_LIST = "resources\\list.txt"

FONT = "arial.ttf"
FONT_SIZE = 60
LOCATION = (2450, 690)


# ------------------- funcs ------------------- #
def read_txt_from_list():
    with open(TODO_LIST) as f:
        return f.read().split('\n')


def update_list(txt):
    with open(TODO_LIST, 'w') as f:
        for line in txt:
            f.write(line)


def draw_txt():
    image = Image.open(os.path.join(sys.path[0], BLANK_BG))  # open img
    draw = ImageDraw.Draw(image)  # create draw object
    font = ImageFont.truetype(FONT, size=FONT_SIZE)

    location = list(LOCATION)
    space = 90

    txt = read_txt_from_list()
    for line in txt:
        draw.text(tuple(location), line, font=font)
        location[1] += space

    image.save(os.path.join(sys.path[0], OUTPUT_BG))


def set_bg():
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(sys.path[0], OUTPUT_BG), 1)


def print_lines():
    print("list:")
    txt = read_txt_from_list()
    for num, line in enumerate(txt):
        print(num, '|', line)
    print('\n')


def modify():
    while True:
        instruction = input("whatcha wanna do? ")
        if instruction == QUIT:
            break
        elif instruction == COMPLETE:
            delete()
        elif instruction == ADD:
            add()
        else:
            print(INVALID_MSG)


def delete():
    while True:
        user_input = input(DELETE_USAGE)
        lines = user_input.split()
        break

    with open(TODO_LIST) as f:
        file_lines = f.readlines()
    with open(TODO_LIST, 'w') as f:
        for num, line in enumerate(file_lines):
            if str(num) not in lines:
                f.write(line)
    print_lines()


def add():
    while True:
        user_input = input(ADD_USAGE)
        clause = user_input.split()
        if len(clause) == 2:
            break

    with open(TODO_LIST) as f:
        file_lines = f.readlines()
    if clause[1] == '\\n':
        clause[1] = ''
    file_lines.insert(int(clause[0]), clause[1] + '\n')
    # file_lines.insert(int(clause[0]), "\n")
    with open(TODO_LIST, 'w') as f:
        for line in file_lines:
            f.write(line)
    print_lines()


# if __name__ == "__main__":
#     print(INSTRUCTIONS)
#
#     # txt = read_txt_from_list()
#     # print(txt)
#     # print_lines()
#     # modify()
#     # delete()
#
#     draw_txt()
#     set_bg()
