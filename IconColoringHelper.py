from PIL import Image, ImageOps
from pathlib import Path
import argparse


def colConv565To24(col):
    colBitsRGB = [5, 6, 5]
    col24 = []
    for i, e in enumerate(reversed(colBitsRGB)):
        temp = col & ((1 << e) - 1)
        temp = temp << (8 - e)
        col24.append(temp)
        col = col >> e
    return tuple(reversed(col24))

def mergeCol(lightColor, darkColor, grayvalue):
    newCol = []
    if type(grayvalue) == tuple:
        grayvalue = grayvalue[0]
    factor = grayvalue / 255
    for i in range(len(lightColor)):
        newCol.append(int(lightColor[i] * factor + darkColor[i] * (1 - factor)))
    return tuple(newCol)


if __name__ == '__main__':
    desc = "Icon coloring tool. Developped by Max Zuidberg, licensed under MPL-2.0."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="Path to the folder containing the image files to process.")
    parser.add_argument("-o", "--output", type=str, required=True,
                        help="Path to the folder for the processed image files. Must not be the input folder. Existing "
                             "files will be overwritten!")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("-g", "--grayscale", action="store_true",
                      help="Convert the input files to grayscale images.")
    mode.add_argument("-n", "--gray_normalized", action="store_true",
                      help="Convert the input files to grayscale images and normalize the value range. "
                           "Your input files likely result in a grayscale range like 30-200. This command "
                           "normalizes the range to the full 0-255. ")
    mode.add_argument("-c", "--color", type=str, nargs=3, metavar=("FORMAT", "DARK_COL", "LIGHT_COL"),
                      help="Colorize the grayscale input files with the given two colors. This parameter requires "
                           "three integer or hex values. "
                           "1: Color format, which can be 16 (5/6/5 bits) or 24 (8/8/8 bits). "
                           "2: \"dark\" replacement color. 3: \"light\" replacement color. "
                           "Requires grayscale input files (use this _after_ converting to grayscale with -g or -n).")

    args = parser.parse_args()

    inputFolder = Path(args.input)
    outputFolder = Path(args.output)

    if not inputFolder.exists():
        parser.error("Input folder does not exist.")

    if outputFolder == inputFolder:
        parser.error("Input and output folder cannot be the same.")

    outputFolder.mkdir(exist_ok=True)

    if args.color:
        for i,c in enumerate(args.color):
            try:
                args.color[i] = int(c)
            except:
                try:
                    args.color[i] = int(c, 16)
                except:
                    parser.error("Color arguments must be integers (can be given in hex format).")
        if not args.color[0] in (16, 24):
            parser.error("Invalid color format (must be 16 or 24).")
        else:
            colorRange = (1 << args.color[0]) - 1
            if args.color[1] > colorRange:
                parser.error("Dark color ({}) out of range ({}).".format(args.color[1], colorRange))
            if args.color[2] > colorRange:
                parser.error("Light color ({}) out of range ({}).".format(args.color[2], colorRange))
        if args.color[0] == 16:
            darkColor  = colConv565To24(args.color[1])
            lightColor = colConv565To24(args.color[2])
        else:
            darkColor  = ((args.color[1] >> 16) & 0xff, (args.color[1] >> 8) & 0xff, args.color[1] & 0xff)
            lightColor = ((args.color[2] >> 16) & 0xff, (args.color[2] >> 8) & 0xff, args.color[2] & 0xff)

    for ip in inputFolder.iterdir():
        if ip.is_file():
            try:
                im = Image.open(ip)
            except:
                print("Could not open input file " + ip.name)
                continue
        else:
            continue

        if args.grayscale or args.gray_normalized:
            im = ImageOps.grayscale(im)
            if args.gray_normalized:
                mi, ma = 255, 0
                for x in range(im.width):
                    for y in range(im.height):
                        p = im.getpixel((x, y))
                        if p > ma:
                            ma = p
                        if p < mi:
                            mi = p
                scale = 255 / (ma - mi)
                for x in range(im.width):
                    for y in range(im.height):
                        im.putpixel((x, y), int((im.getpixel((x, y)) - mi) * scale))
            im.save(str(outputFolder / ip.name))
        else:
            coloredImage = Image.new("RGB", im.size)

            for x in range(coloredImage.size[0]):
                for y in range(coloredImage.size[1]):
                    coloredImage.putpixel((x, y), mergeCol(darkColor=darkColor, lightColor=lightColor, grayvalue=im.getpixel((x, y))))

            coloredImage.save(str(outputFolder / ip.name))

