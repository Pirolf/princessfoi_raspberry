from state import State
from state_name import StateName
from thermal_sensor import ThermalSensor
from robot_controller import RobotController
from graceful_killer import GracefulKiller
from argparse import ArgumentParser
from curtsies import Input
import numpy as np
from time import sleep
from vision.classify import Classifier
from picamera import PiCamera


thermal = ThermalSensor()
controller = RobotController()

state = State(StateName.INIT, controller, {"a": 0})
killer = GracefulKiller(state)
classifier = Classifier('models/MobileNetSSD_deploy.prototxt.txt',
                        'models/MobileNetSSD_deploy.caffemodel')


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


def init(camera):
    camera.resolution = (960, 720)
    camera.framerate = 30
    # warmup time
    sleep(2)
    # Thermal sensor first read will not return a full array
    thermal.read()


def cam_capture(camera):
    image = np.empty((720 * 960 * 3,), dtype=np.uint8)
    camera.capture(image, 'bgr')
    return image.reshape((720, 960, 3))


with PiCamera() as camera, Input(keynames='curses') as input_generator:
    init(camera)
    state.set_state(StateName.SEARCH)

    while True:
        if killer.kill_now:
            print("killing robot")
            break
        '''
        # read sensors
        pixels = thermal.read()
        if args.debug:
            thermal.pretty_print(pixels)

        # if thermal sensor has cat
        cat_detected = is_cat(pixels)
        print("Cat detected = {}".format(cat_detected))
        '''

        (cat_detected, confidence) = classifier.detect(cam_capture(camera))
        print("Cat detected = {}, Confidence = {}".format(cat_detected, confidence))

        if cat_detected:
            state.set_state(StateName.CHASE)

        if (state.state in [StateName.CHASE, StateName.SEARCH]
                and is_close(input_generator)):
            print("close to cat")
            state.set_state(StateName.FILM)

        sleep(0.01)
