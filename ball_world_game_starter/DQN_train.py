from AIplayer import build_model
import gym
import numpy as np
import random
import ball_world_game
import matplotlib.pyplot as plt
from Training_config import args


def train(replay_memory, model, target_model):
    learning_rate = args.learning_rate
    discount_factor = args.discount_factor
    MIN_REPLAY_SIZE = 1000
    batch_size = args.batch_size

    # We won't carry out training if we dont have enough samples, to avoid over-fitting
    if not replay_memory.have_sample(MIN_REPLAY_SIZE):
        return
    # Sample a batch of states from replay memory
    mini_batch = replay_memory.sample(batch_size)
    current_states = np.array([transition[0] for transition in mini_batch])
    # make prediction on current states with main model
    current_qs_list = model.predict(current_states)
    new_current_states = np.array([transition[3] for transition in mini_batch])
    # make prediction on next states with target model
    future_qs_list = target_model.predict(new_current_states)

    X = []
    Y = []
    for index in range(len(mini_batch)):
        observation, action, reward, new_observation, done = mini_batch[index]
        if not done:
            # try to maximize future q value with respect to the target model prediction on next state
            max_future_q = reward + discount_factor * np.max(future_qs_list[index])
        else:
            # there is no next state as the game is terminated
            max_future_q = reward
        # try to update the current q value using Bellman Equation
        current_qs = current_qs_list[index]
        current_qs[action] = (1 - learning_rate) * current_qs[action] + learning_rate * max_future_q

        X.append(observation)
        Y.append(current_qs)
    # Train our model to have X as input and output Y
    model.fit(np.array(X), np.array(Y), batch_size=batch_size, verbose=0, shuffle=True)


class ReplayMemory():
    """
    Each of the experience in Our Replay Memory consists of
    observation, action, reward, new observation and terminate flag
    """
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

    def have_sample(self, batch_size):
        return len(self.memory) >= batch_size


def main(env):
    max_episodes = args.episode
    # Epsilon-greedy Algorithm's parameter
    max_epsilon = args.max_epsilon
    min_epsilon = args.min_epsilon
    epsilon = max_epsilon

    decay = args.decay_rate

    train_step = args.train_step
    update_step = args.update_step
    # Main model
    model = build_model(env.observation_space.sample().shape[0], env.action_space.n)
    # Target model, update every 100 steps
    target_model = build_model(env.observation_space.sample().shape[0], env.action_space.n)
    # Initialize main, target model weight
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
            # Gen a random number, else-part executes more when epsilon decreases with episode
            rand_num = np.random.rand()
            if rand_num <= epsilon:
                action = env.action_space.sample()
            else:
                predicted = model.predict(observation.reshape(1, -1)).reshape(-1)
                action = np.argmax(predicted)

            # Take a move and get the next observation, reward and terminate flag
            new_observation, reward, terminated, info = env.step(action)
            replay_memory.push([observation, action, reward, new_observation, terminated])
            # Train the model for every [train_step] steps or the game is terminated (either win or lose)
            if terminated or steps % train_step == 0:
                train(replay_memory, model, target_model)

            observation = new_observation
            total_training_reward += reward

            if terminated:
                # Print training information after finishing each episode
                print(f'Episode {episode} Total Reward: {total_training_reward:7} Final Reward: {reward:7}')
                # After some steps, update the main model to the target model
                if steps >= update_step:
                    print('Copy model weight to target model....')
                    target_model.set_weights(model.get_weights())

                    steps = 0
                break

        reward_list.append(total_training_reward)
        epsilon_list.append(epsilon)
        # Decay epsilon according to the greedy algorithm
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay * episode)

    print('Finish Training. Saving Model...')
    if args.save_model:
        target_model.save_weights(args.model_name, overwrite=True)

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
    env = gym.make('ball_world_game/env_main-v0', render_mode=args.mode if not args.v else 'test', num_of_obs=args.num_of_obs, num_of_br=args.num_of_br, num_of_acc=args.num_of_acc, ball_initial_speed=args.ball_initial_speed)
    main(env)

