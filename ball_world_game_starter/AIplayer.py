import gym
import pygame
import argparse as args
from pygame.locals import *
import ball_world_game
import random
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
# not sure if the import within calling any agent or method is valid but it does speed up training
speed_up = False
if speed_up:
    import rl.agents

def build_model(states, actions):            # pass states from the envirnment and action into the model
    model = Sequential()
    model.add(Flatten(input_shape=(states,), name="Input_layer"))     # add a flatten layer to the model
    model.add(Dense(128, activation='relu', name="Hidden_layer_1"))         # add a dense layer to the model
    model.add(Dense(24, activation='relu', name="Hidden_layer_2"))
    model.add(Dense(actions, activation='linear', name="Output_layer"))  # last layer output the actions
    model.compile(loss=tf.keras.losses.mae, optimizer=Adam(lr=0.01), metrics=['mae'])
    print(model.summary())

    return model

