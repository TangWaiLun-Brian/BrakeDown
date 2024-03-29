from AIplayer import build_model
import gym
import numpy as np
import random
import ball_world_game
from Testing_config import args

if not args.disable_speed_up:
    import rl.agents
def test(env):
    # construct model
    model = build_model(env.observation_space.sample().shape[0], env.action_space.n)
    # load model (including raise exception framework)
    try:
        model.load_weights(args.model_name)
    except:
        print(f'Error occured when loading {args.model_name}')
        exit()
    # initialize lists and random seed
    collect_list = []
    reward_list = []
    success_list = []
    random_seed = args.seed
    np.random.seed(random_seed)
    for i in range(args.episode):
        # reset environment and total reward
        total_testing_reward = 0
        observation = env.reset(seed=random_seed)
        done = False
        while not done:
            # model takes a move
            predicted = model.predict(observation.reshape(1, -1), verbose=0).reshape(-1)
            action = np.argmax(predicted)
            new_observation, reward, done, info = env.step(action)

            total_testing_reward += reward
            observation = new_observation
        # print info after every episode
        print(f'testing reward: {total_testing_reward: 5} collected brakes: {env.ball.count}')

        collect_list.append(env.ball.count)
        reward_list.append(total_testing_reward)
        success_list.append(env.ball.count >= 5)
        random_seed = np.random.randint(0, 100000)

    # print final result
    print(f'Success Rate: {sum(success_list) / len(success_list): 5} Average Reward: {sum(reward_list) / len(reward_list): 6} Average Collect: {sum(collect_list) / len(collect_list)}')


if __name__ == '__main__':
    env = gym.make('ball_world_game/env_main-v0', render_mode=args.mode if args.v else 'train', num_of_obs=args.num_of_obs,
                   num_of_br=args.num_of_br, num_of_acc=args.num_of_acc, ball_initial_speed=args.ball_initial_speed)
    test(env)
