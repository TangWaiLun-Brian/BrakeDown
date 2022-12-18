import gym
import pygame
import argparse as args
from pygame.locals import *
from AIplayer import dqn_agent
import ball_world_game


parser = args.ArgumentParser()
parser.add_argument('--episode', type=int, default=1)
parser.add_argument('--max_steps', type=int, default=100000)
parser.add_argument('--seed', type=int, default=1)
parser.add_argument('--fps', type=int, default=-1)
# May modify mode for easier testing
parser.add_argument('--mode', type=str, choices=['human', 'human_rand', 'np_array'], default='human')
parser.add_argument('--load_path', type=str, default='dqn_weight.h5f')
arg = parser.parse_args()
env = gym.make('ball_world_game/env_main', mode=arg.mode)
#env = gym.wrappers.TimeLimit(env, max_episode_steps=arg.max_steps)

if arg.fps > 0:
    env.metadata['render_fps'] = arg.fps

env.action_space.seed(arg.seed)
observation = env.reset(seed=arg.seed)

episode = 0
success_episodes = 0
running = True
step = 0

if arg.mode == 'np_array':
    dqn = dqn_agent(env)
    dqn.load_weights(arg.load_path)
while running:
    if arg.mode == 'human':
        pressed_keys = pygame.key.get_pressed()
        action = 1
        if pressed_keys[K_LEFT]:
            action = 0
        if pressed_keys[K_RIGHT]:
            action = 2
    elif arg.mode == 'human_rand':
        # IMPLEMENT RANDOM ACTION
        pass
    elif arg.mode == 'np_array':
        action = dqn.forward(observation)
        print(action.shape)

    ob, rew, terminated, info = env.step(action)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                env.close()
                # pygame.quit()

    if terminated == True:
        env.close()
        running = False