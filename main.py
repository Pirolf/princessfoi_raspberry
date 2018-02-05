from state import State
from state_name import StateName
from thermal_sensor import ThermalSensor
from robot_controller import RobotController 
from graceful_killer import GracefulKiller
from argparse import ArgumentParser
from time import sleep

thermal = ThermalSensor()
controller = RobotController()

state = State(StateName.SEARCH, controller, {"a": 0})
killer = GracefulKiller(state)

state.p()

state.set_var("a", 1)
state.p()

parser = ArgumentParser()
parser.add_argument("--debug", help="Use debug mode")
args = parser.parse_args()

# loop


def is_cat(pixels):
    # TODO: fill this
    return max(pixels) - min(pixels) >= 2.5 and max(pixels) >= 25


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

    sleep(0.01)
