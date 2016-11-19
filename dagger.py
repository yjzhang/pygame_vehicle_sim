from sklearn.linear_model import LogisticRegression

class DaggerModel(object):
    """
    Abstract class for Dagger-trained models
    """

    def __init__(self):
        pass

    def train(self, dataset):
        """
        Given a dataset of (state, action) pairs, this updates the model.
        """
        pass

    def action(self, state):
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
        self.log_reg = LogisticRegression()

    def train(self, dataset):
        pass

    def action(self, state):
        pass

def dagger_train(model):
    pass
