import gym
import random
import argparse as args
import ball_world_game

parser = args.ArgumentParser()
parser.add_argument('--episode', type=int, default=1)
parser.add_argument('--max_steps', type=int, default=100000)
parser.add_argument('--seed', type=int, default=1)
arg = parser.parse_args()
env = gym.make('ball_world_game/env_main')
env = gym.wrappers.TimeLimit(env, max_episode_steps=arg.max_steps)