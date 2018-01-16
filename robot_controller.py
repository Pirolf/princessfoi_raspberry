from a_star import AStar
from time import sleep
import math

# robot wheel to center = 69 mm
ROBOT_RADIUS = 69
WHEEL_RADIUS = 35
WHEEL_TO_MOTOR = 120

# encoder indices
LEFT_FORWARD = 0
LEFT_BACKWARD = 1
RIGHT_FORWARD = 2
RIGHT_BACKWARD = 3

FORWARD = 0
BACKWARD = 1

SPEED = 50
ENCODER_INTERVAL = 0.05

class RobotController:
    def __init__(self):
        self.a_star = AStar()

    def turn_right(self, degrees=90, stop=True):
        self._turn(degrees, stop, 'right')

    def turn_left(self, degrees=90, stop=True):
        self._turn(degrees, stop, 'left')

    def forward(self, distance, stop=True):
        self._move(distance, stop, FORWARD)

    def backward(self, distance, stop=True):
        self._move(distance, stop, BACKWARD)

    def _move(self, distance, stop, direction):
        threshold = self._motor_move(distance)
        if direction == FORWARD:
            a_star.motors(SPEED, SPEED)
        else:
            a_star.motors(-SPEED, -SPEED)

        self._read_encoder_until(threshold, direction)
        if stop:
            a_star.motors(0, 0)

    def _motor_move(self, distance):
        return (distance / (2 * math.pi * WHEEL_RADIUS)) * WHEEL_TO_MOTOR

    def _motor_rotations(self, degrees):
        wheelRotations = ROBOT_RADIUS * (abs(degrees)/360) / WHEEL_RADIUS
        return wheelRotations * WHEEL_TO_MOTOR

    def _read_encoder_until(self, count, index):
        a_star.reset_encoders(False)
        while True:
            sleep(ENCODER_INTERVAL)
            reading = a_star.read_encoders(index)
            if reading >= count:
                print("reading = {}, threshold = {}".format(reading, count))
                a_star.reset_encoders(True)
                break

    def _turn(self, degrees, stop, orientation):
        threshold = _motor_rotations(degrees)
        if orientation == 'left':
            a_star.motors(-SPEED, SPEED)
            _read_encoder_until(threshold, RIGHT_FORWARD)
        else:
            a_star.motors(SPEED, -SPEED)
            _read_encoder_until(threshold, LEFT_FORWARD)

        if stop:
            a_star.motors(0, 0)

c = RobotController()
c.turn_right()
sleep(2)

c.forward(100)
sleep(2)

c.backward(100)
sleep(2)

c.turn_left()