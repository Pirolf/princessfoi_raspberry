from state import State
from state_name import StateName
from thermal_sensor import ThermalSensor
from robot_controller import RobotController
from graceful_killer import GracefulKiller
from argparse import ArgumentParser
from curtsies import Input
import numpy as np
from time import sleep

thermal = ThermalSensor()
controller = RobotController()

state = State(StateName.INIT, controller, {"a": 0})
killer = GracefulKiller(state)

state.p()

state.set_var("a", 1)
state.p()

parser = ArgumentParser()
parser.add_argument("--debug", help="Use debug mode")
args = parser.parse_args()

# loop


def is_cat(pixels):
    return max(pixels) - min(pixels) >= 2.5 or np.mean(pixels) >= 23


def is_close(input_generator):
    # Before distance sensor is wired up, take keyboard input
    for c in input_generator:
        if c == 'f':
            print("Pressed F: Pretend to find cat")
            return True
        else:
            return False
    return False


def init():
    # Thermal sensor first read will not return a full array
    thermal.read()


with Input(keynames='curses') as input_generator:
    init()
    state.set_state(StateName.SEARCH)

    while True:
        if killer.kill_now:
            print("killing robot")
            break

        # read sensors
        pixels = thermal.read()
        if args.debug:
            thermal.pretty_print(pixels)

        # if thermal sensor has cat
        cat_detected = is_cat(pixels)
        print("Cat detected = {}".format(cat_detected))

        if cat_detected:
            print("cat found")
            state.set_state(StateName.CHASE)

        if (state.state in [StateName.CHASE, StateName.SEARCH]
                and is_close(input_generator)):
            print("close to cat")
            state.set_state(StateName.FILM)

        sleep(0.01)
