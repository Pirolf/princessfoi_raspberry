from Adafruit_AMG88xx import Adafruit_AMG88xx
import numpy as np


class ThermalSensor:
    def __init__(self):
        self.sensor = Adafruit_AMG88xx()

    def read(self):
        return np.array(self.sensor.readPixels())
