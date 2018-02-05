from Adafruit_AMG88xx import Adafruit_AMG88xx
import numpy as np
import re

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


class ThermalSensor:
    def __init__(self):
        self.sensor = Adafruit_AMG88xx()

    def read(self):
        return np.array(self.sensor.readPixels())

    def pretty_print(self, pixels):
      minVal = min(pixels)
      maxVal = max(pixels)
      diff = maxVal - minVal
      decoratedPixelStrings = map(lambda index_pixel: self._decorate(index_pixel[0], index_pixel[1]), enumerate(pixels))
      print(''.join(decoratedPixelStrings))
      print('Min = {0}'.format(minVal))
      print('Max = {0}'.format(maxVal))
      print('Diff = {0}'.format(diff))
      print('====================')

    def _clamp(self, n, minn, maxn):
      return max(min(maxn, n), minn)

    def _decorate(self, index, pixel):
      text = re.sub(COLORS_RE + '(.*?)' + RESET_RE, r'\1', str(pixel))
      bucketIndex = int(np.interp(self._clamp(pixel, 18, 28), [18, 28], [0, 5]))
      colorCode = COLORS[BUCKET_COLORS[bucketIndex]]
      color = COLOR_FORMAT.format(colorCode, text, RESET).rjust(16)
      if ((index + 1) % 8 == 0):
          return color + "\n"
      return color
