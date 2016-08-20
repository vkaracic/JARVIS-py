from __future__ import unicode_literals
from os import makedirs, path
import uuid

from django.conf import settings
from django.core.validators import validate_comma_separated_integer_list
from django.db import models
import numpy as np
import tensorflow as tf


class TFModel(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, unique=True)
    file_path = models.FilePathField(blank=True, null=True)
    num_inputs = models.PositiveIntegerField()
    num_outputs = models.PositiveIntegerField()
    num_hidden = models.CharField(validators=[
        validate_comma_separated_integer_list
    ], max_length=255)
    learning_rate = models.FloatField()
    cost = models.CharField(max_length=255)
    optimizer = models.CharField(max_length=255)
    activation = models.CharField(max_length=255)
    trained = models.BooleanField(default=False)

    def generate_file_path(self):
        """Generate a file path to a new model file.

        Additionally creates a new directory named by the ID of the
        model in 'saved_models'.

        Returns:
            A string designating the newly generated file path.
        """
        dir_path = path.join(
            settings.BASE_DIR,
            'saved_models/{}'.format(self.id)
        )
        makedirs(dir_path)
        self.file_path = '{}/model.ckpt'.format(dir_path)
        self.save()
        return self.file_path

    def get_activation_function(self, layer):
        """Gets the right activation function.

        Args:
            layer (tensor): layer to which to assign the activation function.

        Returns
            The activation function.
        """
        if self.activation == 'SIGM':
            return tf.nn.sigmoid(layer)
        elif self.activation == 'TANH':
            return tf.nn.tanh(layer)

    def get_cost_function(self, output_layer, target):
        """Gets the right cost function.

        Args:
            output_layer (tensor): The output layer of the network.
            target (nparray): Array of targets of the network.

        Returns:
            The cost function.
        """
        if self.cost == 'MSE':
            return self._mse(output_layer, target)
        elif self.cost == 'ENTROPY':
            return self._entropy(output_layer, target)

    def get_optimizer(self, cost_function):
        """Gets the right optimizer.

        Args:
            cost_function (tensor): The cost function of the network.

        Returns:
            The optimizer.
        """
        if self.optimizer == 'GD':
            return tf.train.GradientDescentOptimizer(
                self.learning_rate
            ).minimize(cost_function)

    def _mse(self, output_layer, target):
        """ Mean squared error cost function.

        Args:
            output_layer (tensor): The output layer of the network.
            target (DType): Target value

        Returns:
            Mean squared error value.
        """
        return tf.reduce_mean(
            tf.pow(target - output_layer, 2) / self.num_outputs
        )

    def _entropy(self, output_layer, target):
        """ Cross entropy cost function.

        Args:
            output_layer (tensor): The output layer of the network.
            target (DType): Target value

        Returns:
            Cross entropy value.
        """
        return tf.reduce_mean(
            -tf.reduce_sum(target * tf.log(
                output_layer, reduction_indices=1
            )))

    def create_network(self):
        input_data = tf.placeholder(tf.float32, shape=[None, self.num_inputs])
        output_data = tf.placeholder(tf.float32, shape=[None, self.num_outputs])

        hidden = [int(el) for el in self.num_hidden.split(',')]

        weights = {
            'in': tf.Variable(tf.random_normal([self.num_inputs, hidden[0]])),
            'out': tf.Variable(tf.random_normal([hidden[-1], self.num_outputs]))
        }
        biases = {
            'in': tf.Variable(tf.random_normal([hidden[0]])),
            'out': tf.Variable(tf.random_normal([self.num_outputs]))
        }

        layer_in = tf.add(tf.matmul(input_data, weights['in']), biases['in'])
        input_layer = self.get_activation_function(layer_in)
        output_layer = tf.add(tf.matmul(input_layer, weights['out']), biases['out'])
        cost_function = self.get_cost_function(output_layer, output_data)
        optimizer_obj = self.get_optimizer(cost_function)
        return input_data, output_data, cost_function, optimizer_obj

    def train(self, training_data, min_error=None, iterations=100000):
        inputs = []
        outputs = []
        for data in training_data:
            inputs.append(data[0])
            outputs.append(data[1])
        inputs = np.array(inputs)
        outputs = np.array(outputs)

        x, y, cost, optimizer = self.create_network()
        saver = tf.train.Saver()
        with tf.Session() as sess:
            sess.run(tf.initialize_all_variables())
            if self.trained:
                saver.restore(sess, self.file_path)
            for i in xrange(iterations):
                _, c = sess.run(
                    [optimizer, cost],
                    feed_dict={x: inputs, y: outputs}
                )
                if min_error and c < min_error:
                    break
                if i % 5000 == 0:
                    print '{}, {}'.format(i, c)

            file_path = self.file_path or self.generate_file_path()
            saver.save(sess, file_path)
            print 'model saved in: ', file_path

            if not self.trained:
                self.file_path = file_path
                self.trained = True
                self.save()