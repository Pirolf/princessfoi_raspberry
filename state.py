class State:
    def __init__(self, state, controller, initial_params):
        self.state = state
        self.prev_state = None
        self.controller = controller
        self._reset(initial_params)

    def set_state(self, state):
        self.prev_state = self.state
        self.state = state
        if self.prev_state != self.state:
            self.controller.transition(self.prev_state, self.state)

    def set_var(self, key, value):
        # TODO save previous params?
        if key not in self.params:
            print("Error: {} not in params".format(key))
        else:
            self.params[key] = value

    def p(self):
        print("State = {}".format(self.state))
        print("Params = {}".format(self.params))

    def _reset(self, initial_params):
        self.params = initial_params
