import gym
import pygame
import argparse as args
from pygame.locals import *
import ball_world_game


parser = args.ArgumentParser()
parser.add_argument('--episode', type=int, default=1)
parser.add_argument('--max_steps', type=int, default=100000)
parser.add_argument('--seed', type=int, default=1)
parser.add_argument('--fps', type=int, default=-1)
# May modify mode for easier testing
parser.add_argument('--mode', type=str, choices=['human', 'human_rand', 'np_array'], default='human')
arg = parser.parse_args()
env = gym.make('ball_world_game/env_main')
env = gym.wrappers.TimeLimit(env, max_episode_steps=arg.max_steps)

if arg.fps > 0:
    env.metadata['render_fps'] = arg.fps

env.action_space.seed(arg.seed)
observation, info = env.reset(seed=arg.seed)

episode = 0
success_episodes = 0
running = True
step = 0

while running:
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
                # pygame.quit()