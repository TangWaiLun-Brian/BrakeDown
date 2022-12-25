import gym
import pygame
import argparse as args
from pygame.locals import *
import ball_world_game
import random
import numpy as np


parser = args.ArgumentParser()
parser.add_argument('--episode', type=int, default=1)
parser.add_argument('--max_steps', type=int, default=100000)
parser.add_argument('--seed', type=int, default=1)
parser.add_argument('--fps', type=int, default=-1)
# May modify mode for easier testing
parser.add_argument('--mode', type=str, choices=['human', 'human_rand', 'np_array'], default='human')
# Mat modify stage for training and testing
parser.add_argument('--phase', type=str, choices=['train', 'test', 'visual'], default='test')
parser.add_argument('--load_path', type=str, default='')
arg = parser.parse_args()


if __name__ == '__main__':
    env = gym.make('ball_world_game/env_main-v0', render_mode='train')
    env_visual = gym.make('ball_world_game/env_main-v0', render_mode='test')
    print(env.observation_space)
    # env = gym.wrappers.TimeLimit(env, max_episode_steps=arg.max_steps)

    if arg.fps > 0:
        env.metadata['render_fps'] = arg.fps

    episode = 10
    success_episodes = 0
    running = True
    step = 0