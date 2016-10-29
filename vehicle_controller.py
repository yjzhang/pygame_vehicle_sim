import numpy as np
import random

actions = ['FWD', 'BACK', 'LEFT', 'RIGHT']

class VehicleController(object):
    """
    Basic class for a vehicle controller - target
    """

    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.prev_action = 'FWD'

    def next_action(self, target_state=None):
        """
        Calculates the next action for the vehicle.
        """
        if not target_state:
            # random walk
            if random.random() > 0.99:
                action = [random.choice(actions)]
            else:
                action = self.prev_action
            self.prev_action = action
            return action
