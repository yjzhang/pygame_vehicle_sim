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


class NNDaggerModel(DaggerModel):
    """
    Dagger model for simple location states
    """

    def __init__(self, model_file=None, model_params=None):
        self.model1 = Sequential()
        self.model1.add(Dense(50, input_dim=4))
        self.model1.add(Activation('sigmoid'))
        self.model1.add(Dense(32))
        self.model1.add(Activation('sigmoid'))
        self.model1.add(Dense(9))
        self.model1.add(Activation('sigmoid'))
        self.model1.compile(loss='categorical_crossentropy',
                              optimizer='adam')
        self.old_states = []
        self.old_actions = []

    def train(self, states, actions):
        """
        States
        """
        # convert states into simple representation... just the
        # difference between the positions and the headings
        states = [np.concatenate((s[0:2] - s[5:7], s[2:3], s[7:8])) for s in states]
        self.old_states = self.old_states + states
        self.old_actions = self.old_actions + actions
        states = np.vstack(self.old_states)
        actions = np.vstack([encode_action(a) for a in self.old_actions])
        #early_stopping = EarlyStopping(monitor='val_loss', patience=2)
        self.model1.fit(states, actions,
            nb_epoch=50,
            batch_size=500,
            show_accuracy=True)

    def action(self, state, prev_action=None):
        state = np.concatenate((state[0:2] - state[5:7], state[2:3], state[7:8]))
        action = self.model1.predict_classes(np.reshape(state, (1, 4)), verbose=0)
        action = action[0]
        #action = self.model1.predict(np.reshape(state, (1, 4)), verbose=0)[0]
        #print sum(action/(sum(action)+0.000001))
        #action = np.argmax(np.random.multinomial(1, action/(sum(action)+0.000001)))
        #print action
        return decode_action(action)

    def save(self, file_prefix='nn_dagger'):
        model_json = self.model1.to_json()
        with open(file_prefix+'_model.json', 'w') as f:
            f.write(model_json)
        self.model1.save_weights(file_prefix+'_weights.h5')

    def load(self, file_prefix='nn_dagger'):
        self.model1 = model_from_json(open(file_prefix+'_model.json').read())
        self.model1.load_weights(file_prefix+'_weights.h5')
        self.model1.compile(loss='categorical_crossentropy',
                              optimizer='adam')

class NNDaggerLookbackModel(DaggerModel):
    """
    Dagger NN model, but uses the previous action as a state input.
    """

    def __init__(self, model_file=None, model_params=None):
        self.model1 = Sequential()
        self.model1.add(Dense(50, input_dim=4+9))
        self.model1.add(Activation('sigmoid'))
        self.model1.add(Dense(32))
        self.model1.add(Activation('sigmoid'))
        self.model1.add(Dense(9))
        self.model1.add(Activation('sigmoid'))
        self.model1.compile(loss='categorical_crossentropy',
                              optimizer='adam')
        self.old_states = []
        self.old_actions = []
        self.prev_action = np.zeros(9)

    def train(self, states, controls, actions):
        """
        States
        """
        # convert states into simple representation... just the
        # difference between the positions and the headings
        states = [np.concatenate((s[0:2] - s[5:7], s[2:3], s[7:8])) for s in states]
        new_states = []
        for s, a in zip(states[1:], actions[:-1]):
            new_states.append(np.concatenate((s,  encode_action(a))))
        self.old_states = self.old_states + new_states
        self.old_actions = self.old_actions + controls[:-1]
        states = np.vstack(self.old_states)
        actions = np.vstack([encode_action(a) for a in self.old_actions])
        #early_stopping = EarlyStopping(monitor='val_loss', patience=2)
        self.model1.fit(states, actions,
            nb_epoch=50,
            batch_size=500,
            show_accuracy=True)

    def action(self, state, prev_action=None):
        """
        Note: prev_action is in the 2d vector representation.
        """
        state = np.concatenate((state[0:2] - state[5:7], state[2:3], state[7:8]))
        prev_action = encode_action(prev_action)
        state = np.concatenate((state, prev_action))
        action = self.model1.predict(np.reshape(state, (1, 13)), verbose=0)
        action = np.argmax(action[0])
        #action = self.model1.predict(np.reshape(state, (1, 4)), verbose=0)[0]
        #print sum(action/(sum(action)+0.000001))
        #action = np.argmax(np.random.multinomial(1, action/(sum(action)+0.000001)))
        #print action
        return decode_action(action)

    def save(self, file_prefix='nn_dagger_lookback'):
        model_json = self.model1.to_json()
        with open(file_prefix+'_model.json', 'w') as f:
            f.write(model_json)
        self.model1.save_weights(file_prefix+'_weights.h5')

    def load(self, file_prefix='nn_dagger_lookback'):
        self.model1 = model_from_json(open(file_prefix+'_model.json').read())
        self.model1.load_weights(file_prefix+'_weights.h5')
        self.model1.compile(loss='categorical_crossentropy',
                              optimizer='adam')
