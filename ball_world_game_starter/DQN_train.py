from AIplayer import build_model
import gym
import numpy as np
import random
import ball_world_game
import matplotlib.pyplot as plt
from Training_config import args


def train(env, replay_memory, model, target_model, done):
    learning_rate = args.learning_rate
    discount_factor = args.discount_factor
    MIN_REPLAY_SIZE = 1000
    batch_size = args.batch_size

    if not replay_memory.can_provide_sample(MIN_REPLAY_SIZE):
        return

    mini_batch = replay_memory.sample(batch_size)
    current_states = np.array([transition[0] for transition in mini_batch])
    current_qs_list = model.predict(current_states)
    new_current_states = np.array([transition[3] for transition in mini_batch])
    future_qs_list = target_model.predict(new_current_states)

    X = []
    Y = []
    for index, (observation, action, reward, new_observation, done) in enumerate(mini_batch):
        if not done:
            max_future_q = reward + discount_factor * np.max(future_qs_list[index])
        else:
            max_future_q = reward

        current_qs = current_qs_list[index]
        current_qs[action] = (1 - learning_rate) * current_qs[action] + learning_rate * max_future_q

        X.append(observation)
        Y.append(current_qs)
    model.fit(np.array(X), np.array(Y), batch_size=batch_size, verbose=0, shuffle=True)


class ReplayMemory():

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.push_count = 0

    def push(self, experience):
        if len(self.memory) < self.capacity:
            self.memory.append(experience)
        else:
            self.memory[self.push_count % self.capacity] = experience

        self.push_count += 1

    def sample(self, batch_size):
        samples = random.sample(self.memory, batch_size)
        return samples

    def can_provide_sample(self, batch_size):
        return len(self.memory) >= batch_size


def main(env):
    max_episodes = args.episode

    max_epsilon = args.max_epsilon  # You can't explore more than 100% of the time
    min_epsilon = args.min_epsilon  # At a minimum, we'll always explore 1% of the time
    epsilon = max_epsilon  # Epsilon-greedy algorithm in initialized at 1 meaning every step is random at the start

    decay = args.decay_rate

    render = True
    model = build_model(env.observation_space.sample().shape[0], env.action_space.n)
    # Target model, update every 100 steps
    target_model = build_model(env.observation_space.sample().shape[0], env.action_space.n)
    target_model.set_weights(model.get_weights())

    replay_memory = ReplayMemory(args.replay_size)

    reward_list = []
    epsilon_list = []

    steps = 0
    for episode in range(max_episodes):
        total_training_reward = 0
        observation = env.reset(seed=np.random.randint(0, 500000))
        done = False

        while not done:
            steps += 1

            rand_num = np.random.rand()

            if rand_num <= epsilon:
                action = env.action_space.sample()
            else:
                predicted = model.predict(observation.reshape(1, -1)).reshape(-1)
                action = np.argmax(predicted)

            new_observation, reward, terminated, info = env.step(action)
            replay_memory.push([observation, action, reward, new_observation, terminated])

            if steps % 4 == 0 or terminated:
                train(env, replay_memory, model, target_model, terminated)

            observation = new_observation
            total_training_reward += reward

            if terminated:
                print(f'Episode {episode} Total Reward: {total_training_reward:7} Final Reward: {reward:7}')

                if steps >= 100:
                    print('Copy model weight to target model....')
                    target_model.set_weights(model.get_weights())

                    steps = 0
                break

        reward_list.append(total_training_reward)
        epsilon_list.append(epsilon)

        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay * episode)

    print('Finish Training. Saving Model...')
    if args.save_model:
        target_model.save_weights('my_dqn_weight_2.h5', overwrite=True)

    episode_list = np.arange(max_episodes)
    # plot graphs
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(1, 1, 1)
    window_size = 15
    reward_sma = [sum(reward_list[i:i+window_size]) / window_size for i in range(0, len(reward_list)-window_size+1)]
    ax1.plot(np.arange(len(reward_sma)), reward_sma)
    ax1.set_title('SMA Reward over Episodes')

    fig1.savefig('./experimental results/Reward_Graph.png')

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(1, 1, 1)
    ax2.plot(episode_list, epsilon_list)
    ax2.set_title('Epsilon over Episodes')
    fig2.savefig('./experimental results/Epislon_Graph.png')


if __name__ == '__main__':
    env = gym.make('ball_world_game/env_main-v0', render_mode=args.mode, num_of_obs=args.num_of_obs, num_of_br=args.num_of_br, num_of_acc=args.num_of_acc, ball_initial_speed=args.ball_initial_speed)
    main(env)

