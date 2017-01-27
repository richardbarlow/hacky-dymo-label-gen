#!/usr/bin/env python3
import argparse
import code128
import os
from PIL import Image, ImageDraw, ImageFont
from subprocess import check_call

file_dir = os.path.dirname(os.path.realpath(__file__))

def get_args():
    parser = argparse.ArgumentParser("Generate and print barcode label")
    parser.add_argument("partcode")
    parser.add_argument("-n", action="store_true", help="Don't print label")
    return parser.parse_args()


def generate_label(part_code):
    left_margin = 32

    ocr_font = ImageFont.truetype(file_dir + '/OCRA.ttf', 32)
    msg_font = ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf', 16)

    barcode_image = code128.image(part_code, thickness=2, height=32, quiet_zone=False)
    barcode_width, barcode_height = barcode_image.size

    label_width = barcode_width+left_margin+113
    label_image = Image.new('L', (label_width, 64), 255)
    label_image.paste(barcode_image, (left_margin, 0))
    draw = ImageDraw.Draw(label_image)

    text_width, text_height = ocr_font.getsize(part_code)
    part_code_text_position = (((barcode_width-text_width)/2)+left_margin, 34)
    draw.text(part_code_text_position, part_code, font=ocr_font)

    msg1_position = (barcode_width + left_margin + 10, 3)
    msg2_position = (barcode_width + left_margin + 23, 22)
    msg3_position = (barcode_width + left_margin + 20, 40)
    draw.text(msg1_position, "Property of", font=msg_font)
    draw.text(msg2_position, "Student", font=msg_font)
    draw.text(msg3_position, "Robotics", font=msg_font)

    # Hack to stop label printer from trimming margin
    draw.point((0,0))

    return label_image


def print_label(f, wpx, hpx):
    w = wpx * 0.0140625
    h = hpx * 0.0140625
    check_call(["lp", "-o", "PageSize=Custom.{0}x{1}cm".format(h, w), f])


if __name__ == "__main__":
    args = get_args()
    partcode = args.partcode.upper()
    label = generate_label(partcode)
    label_filename = "{0}.png".format(partcode)
    label.save(label_filename)

    if not args.n:
        wpx, hpx = label.size
        print_label(label_filename, wpx, hpx)
