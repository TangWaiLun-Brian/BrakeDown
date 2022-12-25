from Other_DQN_Agent import DQN_Agent, EpsilonGreedyStrategy, ReplayMemory
import gym
import pygame
import argparse as args
from pygame.locals import *
import ball_world_game
import random
import numpy as np

parser = args.ArgumentParser()
parser.add_argument('--max_episode', type=int, default=1)
parser.add_argument('--batch_size', type=int, default=64)
parser.add_argument('--eps_start', default=1)
parser.add_argument('--eps_end', default=0)
parser.add_argument('--decay_rate', default=0.001)
parser.add_argument('--update_target_epoch', default=25)
parser.add_argument('--memory_capacity', default=50000)
parser.add_argument('--learning_rate', default=0.01)
parser.add_argument('--seed', type=int, default=1)
parser.add_argument('--fps', type=int, default=-1)
# May modify mode for easier testing
parser.add_argument('--mode', type=str, choices=['human', 'human_rand', 'np_array'], default='human')
# Mat modify stage for training and testing
parser.add_argument('--phase', type=str, choices=['train', 'test', 'visual'], default='test')
parser.add_argument('--load_path', type=str, default='')
arg = parser.parse_args()

if __name__ == '__main__':
    # initialize environment
    env = gym.make('ball_world_game/env_main-v0', render_mode='train')
    env_visual = gym.make('ball_world_game/env_main-v0', render_mode='test')
    print(env.observation_space.sample().shape)
    # env = gym.wrappers.TimeLimit(env, max_episode_steps=arg.max_steps)

    if arg.fps > 0:
        env.metadata['render_fps'] = arg.fps

    #initialize learning strategy
    strategy = EpsilonGreedyStrategy(arg.eps_start)
