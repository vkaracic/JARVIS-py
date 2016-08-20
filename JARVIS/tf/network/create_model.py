from os.path import join
import numpy as np
import tensorflow as tf

from django.conf import settings

from tf.models import TFModel


class TFNetwork(object):

    def __init__(
            self,
            inputs,
            hidden,
            outputs,
            lr=0.01,
            cost='MSE',
            optim='GD',
            act='SIGM'
    ):
        self.num_inputs = inputs
        self.num_outputs = outputs
        self.num_hidden = hidden
        self.learning_rate = lr
        self.cost = cost
        self.cost_function = None
        self.optimizer = optim
        self.activation = act

    def start(self):
        return TFModel.objects.create(
            num_inputs=self.num_inputs,
            num_outputs=self.num_outputs,
            num_hidden=self._list_to_string(),
            learning_rate=self.learning_rate,
            cost=self.cost,
            optimizer=self.optimizer,
            activation=self.activation,
        )

    def _list_to_string(self):
        return ','.join(str(el) for el in self.num_hidden)
