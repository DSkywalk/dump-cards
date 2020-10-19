#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
dump.py.
Python library to crop cards form PDF

https://github.com/dskywalk/dump-cards

Copyright (C)  2020 dskywalk - http://david.dantoine.org
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 2 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import argparse, os
from pdf2image import convert_from_path

__VERSION__ = '1.0'

X = 0
Y = 1
WIDTH = 2
HEIGHT = 3

def crop_page(image, rect, gap):
  width, height = image.size
  base_x = rect[X]
  base_y = rect[Y]
  crops = []
  while (rect[Y] + rect[HEIGHT] < height):
    while (rect[X] + rect[WIDTH] < width):
      # print ("%u: %u > %u" % (rect[Y], rect[X] + rect[WIDTH], width))
      crop = image.crop((
        rect[X],
        rect[Y],
        rect[X] + rect[WIDTH],
        rect[Y] + rect[HEIGHT]
      ))
      crops.append(crop)
      rect[X] = rect[X] + rect[WIDTH] + gap[X]
    rect[Y] = rect[Y] + rect[HEIGHT] + gap[Y]
    rect[X] = base_x
  rect[Y] = base_y
  return crops

def save_images(output, images, number):
  save_path = os.path.join(output, "page_%04d" % number)
  if not os.path.exists(save_path):
    os.makedirs(save_path)
  n_image = 0
  for image in images:
    image.save(os.path.join(save_path, 'out-%u.png' % n_image), 'PNG')
    n_image += 1

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Process some images on a PDF.')
  parser.add_argument("--file", metavar='file', type=str, help="PDF file to dump")
  parser.add_argument("--rect", metavar='rect', type=str, help="Image crop rectangle (in Pixels). ex: --rect=10,10,50,50")
  parser.add_argument("--gap", metavar='gap', type=str, help="Image gap (in Pixels) title. ex: --gap=20,30")
  parser.add_argument("--output", metavar='output', type=str, help="Image path dump output.")
  parser.add_argument("--first", metavar='first', type=bool, help="Dump only first page for tests sizes.")
  args = parser.parse_args()

  if args.file == None or not os.path.exists(args.file):
    exit("Please specify a valid file using the --file= parameter.")

  if args.output == None or not os.path.exists(args.output):
    exit("Please specify a valid file using the --output= parameter.")

  if args.rect == None:
    exit("Please specify a rect using the --rect= parameter.")

  rect = [int(x.strip(), 10) for x in args.rect.split(',')]
  if len(rect) != 4:
    exit("Please specify a valid rect using the --rect= parameter. Incorrect values or string.")

  print("\n%s Dumping to %s using... (%s)" % (args.file, args.output, str(args.first)))
  print("rect: %s (pixels)" % str(rect))

  gap = [0, 0]
  if args.gap != None:
      tmp = [int(x.strip(), 10) for x in args.gap.split(',')]
      if len(tmp) == 2:
        gap = tmp

  print("gap: %s (pixels)" % str(gap))

  n_page = 0
  pages = convert_from_path(args.file) # , dpi=300

  if args.first == True:
    pages[0].save(os.path.join(args.output, 'out-first.png'), 'PNG')
    exit("Dumped only first page. Exiting!")

  for image in pages:
    print("PAGE: %u" % n_page)
    crops = crop_page(image, rect, gap)
    save_images(args.output, crops, n_page)
    n_page += 1


