from a_star import AStar
from time import sleep
from state_name import StateName
import math

# robot wheel to center = 69 mm
ROBOT_RADIUS = 69
WHEEL_RADIUS = 35
WHEEL_TO_MOTOR = 120

# encoder indices
STATIONARY = -1
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
        self.reset_encoder_states()

    def transition(self, prev_state, state):
        if state == StateName.CHASE:
            print("CHASE")
            self.a_star.motors(SPEED, SPEED)
        elif state == StateName.SEARCH:
            print("SEARCH: start rotating")
            self.a_star.motors(SPEED, -SPEED)
        elif state == StateName.TERMINATE:
            print("TERMINATE: stop the robot")
            self.a_star.motors(0, 0)

        return

    def reset_encoder_states(self):
        self.encoders = (0, 0, 0, 0)
        self.threshold = float('inf')
        self.encoder_index = STATIONARY
        self.a_star.reset_encoders(True)

    def update(self):
        self.encoders = a_star.read_encoders()
        if self.encoders[encoder_index] >= threshold:
            print("stopping motors at threshold = {}".format(threshold))
            self.reset_encoder_states()
            return True
        return False

    def turn_right(self, degrees=90, stop=True):
        self.threshold = self._motor_rotations(degrees)
        self.encoder_index = LEFT_FORWARD
        self.a_star.reset_encoders(False)
        self.a_star.motors(SPEED, -SPEED)

    def turn_left(self, degrees=90, stop=True):
        self.threshold = _motor_rotations(degrees)
        self.encoder_index = LEFT_FORWARD
        self.a_star.reset_encoders(False)
        self.a_star.motors(SPEED, -SPEED)

    def turn_left(self, degrees=90, stop=True):
        self._turn(degrees, stop, 'left')

    def forward(self, distance, stop=True):
        self._move(distance, stop, FORWARD)

    def backward(self, distance, stop=True):
        self._move(distance, stop, BACKWARD)

    def _move(self, distance, stop, direction):
        threshold = self._motor_move(distance)
        if direction == FORWARD:
            self.a_star.motors(SPEED, SPEED)
        else:
            self.a_star.motors(-SPEED, -SPEED)

        self._read_encoder_until(threshold, direction)
        if stop:
            self.a_star.motors(0, 0)

    def _motor_move(self, distance):
        return (distance / (2 * math.pi * WHEEL_RADIUS)) * WHEEL_TO_MOTOR

    def _motor_rotations(self, degrees):
        wheelRotations = ROBOT_RADIUS * (abs(degrees)/360) / WHEEL_RADIUS
        return wheelRotations * WHEEL_TO_MOTOR

    def _read_encoder_until(self, count, index):
        self.a_star.reset_encoders(False)
        while True:
            sleep(ENCODER_INTERVAL)
            reading = self.a_star.read_encoders(index)
            if reading >= count:
                print("reading = {}, threshold = {}".format(reading, count))
                self.a_star.reset_encoders(True)
                break

    def _turn(self, degrees, stop, orientation):
        threshold = self._motor_rotations(degrees)
        if orientation == 'left':
            self.a_star.motors(-SPEED, SPEED)
            self._read_encoder_until(threshold, RIGHT_FORWARD)
        else:
            self.a_star.motors(SPEED, -SPEED)
            self._read_encoder_until(threshold, LEFT_FORWARD)

        if stop:
            self.a_star.motors(0, 0)
