import random

import numpy as np
import pygame

import dagger

actions = ['FWD', 'BACK', 'LEFT', 'RIGHT']

class VehicleController(object):
    """
    Basic class for a vehicle controller - target
    """

    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.prev_action = 'FWD'

    def next_action(self, state=None):
        """
        Calculates the next action for the vehicle.
        state: (vehicle1_state, vehicle2_state)
        """
        if not state:
            # random walk
            if random.random() > 0.99:
                action = [random.choice(actions)]
            else:
                action = self.prev_action
            self.prev_action = action
            return [action]

class UserController(VehicleController):
    """
    Controller that has user input...
    """

    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.prev_action = 'FWD'
        self.control_history = []
        self.state_history = []

    def next_action(self, state=None):
        control = []
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        #print [i for i in keys if i>0]
        if keys[pygame.K_UP]:
            control.append('FWD')
        if keys[pygame.K_LEFT]:
            control.append('LEFT')
        if keys[pygame.K_DOWN]:
            control.append('BACK')
        if keys[pygame.K_RIGHT]:
            control.append('RIGHT')
        self.state_history.append(state)
        self.control_history.append(control)
        return control

class BasicEvasionController(VehicleController):
    """
    Always travels away from the pursuer.
    """

    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.prev_action = 'FWD'

    def next_action(self, state=None):
        """
        state: (self vehicle state, other vehicle state)
        """
        control = []
        self_state = state[0]
        other_state = state[1]
        return control
