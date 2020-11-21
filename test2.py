from PIL import Image, ImageDraw, ImageFont


def draw_underlined_text(draw, pos, text, font, **options):
    twidth, theight = draw.textsize(text, font=font)
    lx, ly = pos[0], pos[1] + theight
    draw.text(pos, text, font=font, **options)
    draw.line((lx, ly, lx + twidth, ly, lx+60, ly+60), **options)

if __name__ == "__main__":
    im = Image.new('RGB', (400, 400), (255,) * 3)
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("arial.ttf", 50)

    draw_underlined_text(draw, (50, 150), 'Hello PIL!', font, fill=0)
    draw_underlined_text(draw, (50, 300), 'Test', font, fill=128)


    draw.line((0, 0) + im.size, fill=500, width=10)
    # draw.line((0, im.size[1], im.size[0], 0), fill=128)

    im.show()
