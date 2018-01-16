#!/usr/bin/python
# Copyright (c) 2017 Adafruit Industries
# Author: Dean Miller
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

from Adafruit_AMG88xx import Adafruit_AMG88xx
from time import sleep
import numpy as np
import re
#import Adafruit_AMG88xx.Adafruit_AMG88xx as AMG88

# Default constructor will pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
#
# For the Beaglebone Black the library will assume bus 1 by default, which is
# exposed with SCL = P9_19 and SDA = P9_20.
sensor = Adafruit_AMG88xx()

# Optionally you can override the bus number:
#sensor = AMG88.Adafruit_AMG88xx(busnum=2)

#wait for it to boot

COLORS = {
  'black': 30,
  'grey': 30, # is actually black
  'red': 31,
  'green': 32,
  'yellow': 33,
  'blue': 34,
  'magenta': 35,
  'cyan': 36,
  'light_grey': 37,
  'dark_grey': 90,
  'light_red': 91,
  'light_green': 92,
  'light_yellow': 93,
  'light_blue': 94,
  'light_magenta': 95,
  'light_cyan': 96,
  'white': 97,
}

BUCKET_COLORS = ['blue', 'cyan', 'green',
  'yellow', 'magenta', 'red']


COLORS_RE = '\033\[(?:%s)m' % '|'.join(['%d' % v for v in COLORS.values()])
RESET_RE = '\033\[0m'

COLOR_FORMAT = '\033[{0}m{1}{2}'
RESET = '\033[0m'

def clamp(n, minn, maxn):
  return max(min(maxn, n), minn)

def decorate(index, pixel):
  text = re.sub(COLORS_RE + '(.*?)' + RESET_RE, r'\1', str(pixel))
  bucketIndex = int(np.interp(clamp(pixel, 18, 28), [18, 28], [0, 5]))
  colorCode = COLORS[BUCKET_COLORS[bucketIndex]]
  color = COLOR_FORMAT.format(colorCode, text, RESET).rjust(16)
  if ((index + 1) % 8 == 0):
      return color + "\n"
  return color

# Main
sleep(.1)
while(1):
  pixels = sensor.readPixels()
  minVal = min(pixels)
  maxVal = max(pixels)
  diff = maxVal - minVal
  decoratedPixelStrings = map(lambda (i,p): decorate(i,p), enumerate(pixels))
  print(''.join(decoratedPixelStrings))
  print('Min = {0}'.format(minVal))
  print('Max = {0}'.format(maxVal))
  print('Diff = {0}'.format(diff))
  print('====================')

  sleep(1)