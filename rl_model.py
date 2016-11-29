import numpy as np

from keras.models import Sequential, model_from_json
from keras.layers import Convolution1D, LSTM, GRU, Dense, Activation, Dropout, MaxPooling1D, Flatten, GlobalAveragePooling1D
from keras.callbacks import EarlyStopping

from dagger import DaggerModel

def encode_action(action):
    """
    Encodes an action (a pair of integers) into a single 9-d array.
    """
    output = np.zeros(9)
    position = action[0] + 3*action[1]
    output[position] = 1.0
    return output

def decode_action(action):
    """
    Converts a single integer into a pair of integers.
    """
    output = [0,0]
    output[0] = action%3
    output[1] = action/3
    return output

def pursuit_reward(state, k=100.0):
    """
    Reward function for the pursuit model.

    Reward function is k/distance - 1.
    """
    p1 = state[0:2]
    p2 = state[5:7]
    dist = np.sqrt(np.dot(p2-p1, p2-p1))
    return k/dist - 1.0


class DeepQModel(DaggerModel):
    """
    Deep Q-learning model
    """

    def __init__(self, model_file=None, model_params=None):
        self.model1 = Sequential()
        self.model1.add(Dense(50, input_dim=4))
        self.model1.add(Activation('sigmoid'))
        self.model1.add(Dense(32))
        self.model1.add(Activation('sigmoid'))
        self.model1.add(Dense(9))
        # output is the Q-value for each action.
        self.model1.compile(loss='mean_squared_error',
                              optimizer='adam')
        self.old_states = []
        self.old_actions = []
        self.old_rewards = []
        self.discount = 0.5

    def get_q_value(self, state, action, reward, state_is_terminal=False):
        """
        Gets the Q-value for one particular action

        if the state is a terminal state:
        """

    def train(self, states, actions, rewards):
        """
        Training should be done at the end of each iteration, or after 500
        steps if the goal has not been reached.
        """
        # convert states into simple representation... just the
        # difference between the positions and the headings
        states = [np.concatenate((s[0:2] - s[5:7], s[2:3], s[7:8])) for s in states]
        self.old_states = self.old_states + states
        self.old_actions = self.old_actions + actions
        states = np.vstack(self.old_states)
        actions = np.vstack([encode_action(a) for a in self.old_actions])
        #early_stopping = EarlyStopping(monitor='val_loss', patience=2)
        # TODO: create a 9-d map of rewards and actions
        # actually, no, actions to q-values for each position...
        self.model1.fit(states, actions,
            nb_epoch=50,
            batch_size=500,
            show_accuracy=True)

    def action(self, state):
        state = np.concatenate((state[0:2] - state[5:7], state[2:3], state[7:8]))
        action = self.model1.predict_classes(np.reshape(state, (1, 4)), verbose=0)
        action = action[0]
        #action = self.model1.predict(np.reshape(state, (1, 4)), verbose=0)[0]
        #print sum(action/(sum(action)+0.000001))
        #action = np.argmax(np.random.multinomial(1, action/(sum(action)+0.000001)))
        #print action
        return decode_action(action)

    def save(self, file_prefix='deepq'):
        model_json = self.model1.to_json()
        with open(file_prefix+'_model.json', 'w') as f:
            f.write(model_json)
        self.model1.save_weights(file_prefix+'_weights.h5')

    def load(self, file_prefix='deepq'):
        self.model1 = model_from_json(open(file_prefix+'_model.json').read())
        self.model1.load_weights(file_prefix+'_weights.h5')
        self.model1.compile(loss='mean_squared_error',
                              optimizer='adam')
