import numpy as np
from sklearn.linear_model import LogisticRegression

class DaggerModel(object):
    """
    Abstract class for Dagger-trained models
    """

    def __init__(self):
        pass

    def train(self, states, actions):
        """
        Given a dataset of (state, action) pairs, this updates the model.
        """
        pass

    def action(self, state, prev_action=None):
        """
        Given a current state, gives the next action.
        """
        pass

class LinearDaggerModel(DaggerModel):
    """
    A Dagger model that uses multiclass logistic regression to generate
    its actions.
    """

    def __init__(self):
        self.movement = LogisticRegression(solver='sag', multi_class='multinomial')
        self.turn = LogisticRegression(solver='sag', multi_class='multinomial')
        self.old_states = []
        self.old_actions = []

    def train(self, states, actions):
        """
        states: list of 10-d vectors
        actions: list of pairs of integers - one for fwd/back, one for left/right
        """
        states = self.old_states + states
        self.old_states = states
        actions = self.old_actions + actions
        self.old_actions = actions
        states = np.vstack(states)
        actions1 = np.vstack([a[0] for a in actions])
        actions2 = np.vstack([a[1] for a in actions])
        self.movement.fit(states, actions1)
        self.turn.fit(states, actions2)

    def action(self, state, prev_action=None):
        m = self.movement.predict(state)
        t = self.turn.predict(state)
        return (m, t)

