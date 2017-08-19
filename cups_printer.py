#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by vellhe 2017/8/18
# import cups

# img_path = "test.png"
# conn = cups.Connection()
# printers = conn.getPrinters()
# printer_name = printers.keys()[0]
# cups.setUser('pi')
# width = 58
# length = 58
# # conn.printFile(printer_name, img_path, 'print_img', options={'media': 'Custom.%dx%dmm' % (width, length)})
# conn.printFile(printer_name, img_path, 'print_img', options={'media': 'Custom.%dx%dmm' % (width, length),
#                                                              'sides': 'two-sided-long-edge'
#                                                              })
# # conn.printFile(printer_name, img_path, 'print_img', options={'media': '48mmx40mm',
# #                                                              'sides': 'two-sided-long-edge'
# #                                                              })
# conn.printFile(printer_name, img_path, 'print_img', options={'media': '48mmx10mm'})
import os
import subprocess

from PIL import Image


def print_img(img_path):
    if not os.path.exists(img_path):
        print("img_path not exist")
        return False

    img_path = os.path.abspath(img_path)
    img = Image.open(img_path)
    size = img.size
    height = int(48.0 / size[0] * size[1])
    status = subprocess.call(['lpr', '-o', 'media=Custom.48x%dmm' % height, img_path])
    if status == 0:
        print("print succ")
        return True
    else:
        print("print error, status: %d" % status)
        return False


if __name__ == "__main__":
    print_img("./out.jpg")
