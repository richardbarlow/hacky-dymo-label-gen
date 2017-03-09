#!/usr/bin/env python3
import argparse
import code128
import os
from PIL import Image, ImageDraw, ImageFont
from subprocess import check_call

file_dir = os.path.dirname(os.path.realpath(__file__))

def get_args():
    parser = argparse.ArgumentParser("Generate and print barcode label")
    parser.add_argument("mac")
    parser.add_argument("-n", action="store_true", help="Don't print label")
    return parser.parse_args()


def generate_label(macaddr):
    left_margin = 32

    ocr_font = ImageFont.truetype(file_dir + '/OCRA.ttf', 20)

    line1 = macaddr[:8]
    line2 = macaddr[9:]
    line_width, line_height = ocr_font.getsize(line1)

    label_width = left_margin+line_width
    label_image = Image.new('L', (label_width, 64), 255)
    draw = ImageDraw.Draw(label_image)

    line1_position = (left_margin, 4)
    line2_position = (left_margin, 36)
    draw.text(line1_position, line1, font=ocr_font)
    draw.text(line2_position, line2, font=ocr_font)

    # Hack to stop label printer from trimming margin
    draw.point((0,0))

    return label_image


def print_label(f, wpx, hpx):
    w = wpx * 0.0140625
    h = hpx * 0.0140625
    check_call(["lp", "-o", "PageSize=Custom.{0}x{1}cm".format(h, w), f])


if __name__ == "__main__":
    args = get_args()
    mac = args.mac.upper()
    if len(mac) != 17:
        print("mac address must be 17 characters long (inc. :)")
        exit(1)
    label = generate_label(mac)
    label_filename = "{0}.png".format(mac.replace(":","-"))
    label.save(label_filename)

    if not args.n:
        wpx, hpx = label.size
        print_label(label_filename, wpx, hpx)
