import random

import numpy as np
import pygame

import dagger

actions = ['FWD', 'BACK', 'LEFT', 'RIGHT']

def normalize_angle(ang):
    if ang<0:
        ang = ang%(2*np.pi)
        ang = 2*np.pi + ang
    return ang%(2*np.pi)

def action_to_vecs(action):
    a1 = 0
    if 'FWD' in action:
        a1 = 1
    elif 'BACK' in action:
        a1 = 2
    a2 = 0
    if 'LEFT' in action:
        a2 = 1
    elif 'RIGHT' in action:
        a2 = 2
    return (a1, a2)

def vecs_to_action(vecs):
    a1 = vecs[0]
    a2 = vecs[1]
    action = []
    if a1 == 1:
        action.append('FWD')
    elif a1 == 2:
        action.append('BACK')
    if a2 == 1:
        action.append('LEFT')
    elif a2 == 2:
        action.append('RIGHT')
    return action

class VehicleController(object):
    """
    Basic class for a vehicle controller - target
    """

    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.prev_action = ['FWD']

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
            return action

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
        pos_diff = [self_state[0]-other_state[0], self_state[1]-other_state[1]]
        heading_diff = normalize_angle(self_state[2]) - normalize_angle(other_state[2])
        # note: normalize heading_diff to be between pi and -pi
        # print heading_diff
        if heading_diff < 0 and np.abs(heading_diff) < np.pi/2:
            control.append('LEFT')
        elif heading_diff > 0 and heading_diff < np.pi/2:
            control.append('RIGHT')
        control.append('FWD')
        return control

class DaggerPursuitController(VehicleController):
    """
    Controller that has dummy user input...
    """

    def __init__(self, vehicle, model=None):
        self.vehicle = vehicle
        self.prev_action = 'FWD'
        self.control_history = []
        self.state_history = []
        self.model = model
        # controls: 'policy_learn', 'user', 'policy'
        self.control = 'user'
        self.round = 0

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
        state = np.concatenate((state[0], state[1]))
        self.state_history.append(state)
        if self.control=='policy_learn':
            action = vecs_to_action(self.model.action(state))
            # basically, if no key is pressed then we're implicitly agreeing
            # with the provided policy.
            if control or keys[pygame.K_SPACE]:
                self.control_history.append(action_to_vecs(control))
            else:
                self.control_history.append(action_to_vecs(action))
            return action
        else:
            self.control_history.append(action_to_vecs(control))
            return control

    def train(self):
        """
        Resets the round, trains using the new data
        """
        self.model.train(self.state_history, self.control_history)
        self.control_history = []
        self.state_history = []
        self.round += 1


class DaggerEvasionController(VehicleController):
    """
    Controller that has dummy user input...
    """

    def __init__(self, vehicle, model=None):
        self.vehicle = vehicle
        self.prev_action = 'FWD'
        self.control_history = []
        self.state_history = []
        self.model = model
        self.control = 'policy'

    def next_action(self, state=None):
        control = []
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        #print [i for i in keys if i>0]
        if keys[pygame.K_W]:
            control.append('FWD')
        if keys[pygame.K_A]:
            control.append('LEFT')
        if keys[pygame.K_S]:
            control.append('BACK')
        if keys[pygame.K_D]:
            control.append('RIGHT')
        self.state_history.append(state)
        self.control_history.append(control)
        if self.control=='policy':
            return self.model.action(state)
        else:
            return control
