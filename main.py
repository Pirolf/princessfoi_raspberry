from state import State
from state_name import StateName
from thermal_sensor import ThermalSensor
from time import sleep
import numpy as np

state = State(StateName.SEARCH, {"a": 0})
state.p()

state.set_var("a", 1)
state.p()

thermal = ThermalSensor()
# loop


def is_cat(pixels):
    # TODO: fill this
    return np.any(pixels) > 23


while True:
    # read sensors
    pixels = thermal.read()

    # if thermal sensor has cat
    if is_cat(pixels):
        print("cat found")
        state.set_name(StateName.CHASE)

    sleep(0.01)
