from thermal_sensor import ThermalSensor
from a_star import AStar
from time import sleep
from curtsies import Input


def is_cat(pixels):
    return max(pixels) - min(pixels) >= 2.5 and max(pixels) >= 25


thermal = ThermalSensor()
aStar = AStar()
SPEED = 50

with Input(keynames='curses') as input_generator:
    while True:
        pixels = thermal.read()
        thermal.pretty_print(pixels)

        print("Is cat? {}".format(is_cat(pixels)))
        for c in input_generator:
            if c == 'w':
                print("Pressed W: Forward")
                aStar.motors(SPEED, SPEED)
            elif c == "s":
                print("Pressed S: Backward")
                aStar.motors(-SPEED, -SPEED)
            elif c == "q":
                print("Pressed Q: Turn Left")
                aStar.motors(-SPEED, SPEED)
            elif c == "e":
                print("Pressed E: Turn Right")
                aStar.motors(SPEED, -SPEED)
            elif c == "z":
                print("Pressed Z: Stop")
                aStar.motors(0, 0)
            elif c == '<ESC>':
                break

        sleep(0.1)
