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
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

print(tf.__version__)
print(Adam)
print(tf.optimizers.Adam)
parser = args.ArgumentParser()
parser.add_argument('--episode', type=int, default=1)
parser.add_argument('--max_steps', type=int, default=100000)
parser.add_argument('--seed', type=int, default=1)
parser.add_argument('--fps', type=int, default=-1)
# May modify mode for easier testing
parser.add_argument('--mode', type=str, choices=['human', 'human_rand', 'np_array'], default='human')
arg = parser.parse_args()
env = gym.make('ball_world_game/env_main', render_mode = False, mode='AI')
#env = gym.wrappers.TimeLimit(env, max_episode_steps=arg.max_steps)

if arg.fps > 0:
    env.metadata['render_fps'] = arg.fps



episode = 10
success_episodes = 0
running = True
step = 0


# Random Movement

total_score = 0
 

# for episode in range(1, episode+1):
#     env.action_space.seed(arg.seed)
#     observation = env.reset(seed=arg.seed)
#     done = False
#     score = 0
#
#
#     while not done:
#         #env.render()        # visualize the state
#         action = random.choice([0,1,2])       # randomly choose the action
#         ob, rew, terminated, truncated, info = env.step(action)  #return the value after the action
#         score += rew                    # calculate the culmulative score
#         done = terminated
#
#
#     total_score += score
#     print(f"Episode:{episode} Score:{score}")


print(f"Average score: {total_score/episode}")
#env.close()



# AI Training part



def build_model(states, actions):            # pass states from the envirnment and action into the model
    model = Sequential()
    model.add(Flatten(input_shape=(1, states), name="Input_layer"))     # add a flatten layer to the model
    model.add(Dense(24, activation='relu', name="Hidden_layer_1"))         # add a dense layer to the model
    model.add(Dense(24, activation='relu', name="Hidden_layer_2"))
    model.add(Dense(actions, activation='linear', name="Output_layer"))  # last layer output the actions
    return model


print('obs shape:', env.observation_space)
states = env.observation_space.shape[0]
actions = env.action_space.n

model = build_model(states, actions)

del model

model = build_model(states, actions)

print(model.summary())

def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy, nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-2)

    return dqn

#obs = env.reset()
#obs2, _, _, _ = env.step(0)
#print(obs.shape, obs2.shape)
dqn = build_agent(model, actions)
#Adam._name = 'No name'
dqn.compile(Adam(learning_rate=1e-3), metrics=['mae'])
dqn.fit(env, nb_steps=10000, visualize=False, verbose=1)

scores = dqn.test(env, nb_episodes=100, visualize=False)
print(np.mean(scores.history['episode_reward']))
dqn.save_weights('dqn_weight.h5f', overwrite=True)
"""while running:
    if arg.mode == 'human':
        pressed_keys = pygame.key.get_pressed()
        action = 1
        if pressed_keys[K_LEFT]:
            action = 0
        if pressed_keys[K_RIGHT]:
            action = 2
    else:
        # IMPLEMENT RANDOM ACTION
        pass

    ob, rew, terminated, truncated, info = env.step(action)

    if terminated == True:
        env.close()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                env.close()
                # pygame.quit()"""