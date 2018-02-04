from Adafruit_AMG88xx import Adafruit_AMG88xx


class TermalSensor:
    def __init__(self):
        self.sensor = Adafruit_AMG88xx()

    def read(self):
        return self.sensor.readPixels()
