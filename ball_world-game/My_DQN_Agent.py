import gym
import time
import math
import random
import itertools
import numpy as np
import tensorflow as tf
from statistics import mean
from collections import deque, namedtuple
import tensorflow.keras.layers as kl
import tensorflow.keras.models as km
import tensorflow.keras.optimizers as ko
import tensorflow.keras.losses as kls
from tensorflow.keras.callbacks import TensorBoard

# Initialize tensorboard object
name = f'DQN_logs_{time.time()}'
summary_writer = tf.summary.create_file_writer(logdir=f'logs/{name}/')


class Model(tf.keras.Model):
    """
    Subclassing a multi-layered NN using Keras from Tensorflow
    """

    def __init__(self, input_shape, output_shape):
        # initialize the parent class
        super().__init__()
        self.input_layer = kl.InputLayer(input_shape=(input_shape,))
        intermediate_layer_shape = [128, 24]
        self.intermediate_layers = []

        for intermediate in intermediate_layer_shape:
            self.intermediate_layers.append(kl.Dense(intermediate, activation='relu'))  # Left kernel initializer

        self.output_layer = kl.Dense(output_shape, activation='linear')

    @tf.function
    def call(self, inputs, **kwargs):
        x = self.input_layer(inputs)
        for layer in self.intermediate_layers:
            x = layer(x)
        output = self.output_layer(x)
        return output


class ReplayMemory():
    """
    Used to store the experience genrated by the agent over time
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = None
        self.push_count = 0

    def push(self, experience):
        if self.memory is None:
            self.memory = experience.reshape(1, -1)
        elif self.memory.shape[0] < self.capacity:
            self.memory = np.concatenate([self.memory, experience.reshape(1, -1)], axis=0)
        else:
            self.memory[self.push_count] = experience

        self.push_count += 1

    def sample(self, batch_size):
        index = random.sample(list(range(self.memory.shape[0])), batch_size)
        return self.memory[index]

    def can_provide_sample(self, batch_size):
        return self.memory is not None and self.memory.shape[0] >= batch_size


class EpsilonGreedyStrategy():
    """
    Decaying Epsilon-greedy strategy
    """

    def __init__(self, start, end, decay):
        self.start = start
        self.end = end
        self.decay = decay

    def get_exploration_rate(self, current_step):
        return self.end + (self.start - self.end) * math.exp(-1 * current_step * self.decay)


class DQN_Agent():
    """
    Used to take actions by using the Model and given strategy.
    Flag indicates whether the random choosing is called (More Random at first for exploration, Agent dominates after some time)
    """

    def __init__(self, strategy, num_actions):
        self.current_step = 0
        self.strategy = strategy
        self.num_actions = num_actions

    def select_action(self, state, policy_net):
        rate = self.strategy.get_exploration_rate(self.current_step)
        self.current_step += 1

        if rate > random.random():
            return random.randint(0, self.num_actions-1), rate, True
        else:
            if state.ndim < 2:
                state = state.reshape(1, -1)
            state = state
            output = policy_net(state.astype(np.float32))

            # return: choose optimal action, learning rate, flag
            return np.argmax(output), rate, False


def copy_weights(Copy_from, Copy_to):
    """
    Function to copy weights of a model to other
    """
    variables2 = Copy_from.trainable_variables
    variables1 = Copy_to.trainable_variables
    for v1, v2 in zip(variables1, variables2):
        v1.assign(v2.numpy())

