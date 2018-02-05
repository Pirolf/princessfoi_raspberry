import signal
from state_name import StateName
from state import State
from time import sleep

class GracefulKiller:
    kill_now = False

    def __init__(self, state):
        signal.signal(signal.SIGINT, self.exit_handler(state))
        signal.signal(signal.SIGTERM, self.exit_handler(state))

    def exit_handler(self, state):
        def exit(signum, frame):
            state.set_state(StateName.TERMINATE)
            sleep(0.5)
            self.kill_now = True

        return exit
