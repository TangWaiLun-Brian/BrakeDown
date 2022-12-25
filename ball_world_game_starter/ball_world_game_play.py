import gym
import pygame
import numpy as np
import argparse as args
from pygame.locals import *
from Play_config import args
import ball_world_game

def main(env):
    if args.fps > 0:
        env.metadata['render_fps'] = args.fps

    env.action_space.seed(args.seed)

    collect_list = []
    success_list = []

    random_seed = args.seed
    np.random.seed(random_seed)



    for i in range(args.episode):
        total_testing_reward = 0
        observation = env.reset(seed=random_seed)

        if args.mode == 'human_rand':
            env.action_space.seed(random_seed)

        render = True
        done = False
        while not done:
            # if render:
            #    env.render()
            if args.mode == 'human':
                pressed_keys = pygame.key.get_pressed()
                action = 1
                if pressed_keys[K_LEFT]:
                    action = 0
                if pressed_keys[K_RIGHT]:
                    action = 2
            else:
                action = env.action_space.sample()

            new_observation, reward, done, info = env.step(action)

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        env.close()
                        # pygame.quit()

        print(f'Episode {i} collected brakes: {env.ball.count}')
        collect_list.append(env.ball.count)
        success_list.append(env.ball.count >= 5)
        random_seed = np.random.randint(0, 100000)

    print(f'Success Rate: {sum(success_list) / len(success_list): .2f} Average Collect: {sum(collect_list) / len(collect_list)}')


if __name__ == '__main__':
    env = gym.make('ball_world_game/env_main-v0', render_mode=args.mode, num_of_obs=args.num_of_obs,
                   num_of_br=args.num_of_br, num_of_acc=args.num_of_acc, ball_initial_speed=args.ball_initial_speed)
    main(env)