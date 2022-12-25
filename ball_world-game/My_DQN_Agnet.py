from AIplayer import build_model
import gym
import numpy as np
import random
import ball_world_game

env = gym.make('ball_world_game/env_main-v0', render_mode='test')
env_visual = gym.make('ball_world_game/env_main-v0', render_mode='test')
model = build_model(env.observation_space.sample().shape[0], env.action_space.n)


def train(env, replay_memory, model, target_model, done):
    learning_rate = 0.7
    discount_factor = 0.62
    MIN_REPLAY_SIZE = 1000
    batch_size = 64

    if not replay_memory.can_provide_sample(MIN_REPLAY_SIZE):
        return

    #index = np.random.choice(replay_memory.shape[0], batch_size, replace=False)
    mini_batch = replay_memory.sample(batch_size)
    #mini_batch = random.sample(replay_memory, batch_size)
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

def test():
    model = build_model(env.observation_space.sample().shape[0], env.action_space.n)
    model.load_weights('my_dqn_weight.h5')
    collect_list = []
    reward_list = []
    success_list = []
    for i in range(10):
        total_testing_reward = 0
        observation = env.reset(seed=np.random.randint(0, 500000))
        render = True
        done = False
        while not done:
            if render:
                env.render()
            predicted = model.predict(observation.reshape(1, -1)).reshape(-1)
            action = np.argmax(predicted)
            new_observation, reward, done, info = env.step(action)

            total_testing_reward += reward
            observation = new_observation
        print(f'testing reward: {total_testing_reward: 5} collected brakes: {env.ball.count}')
        collect_list.append(env.ball.count)
        reward_list.append(total_testing_reward)
        success_list.append(env.ball.count >= 5)
    print(f'Success Rate: {sum(success_list) / len(success_list): 5} Average Reward: {sum(reward_list) / len(reward_list): 6} Average Collect: {sum(collect_list) / len(collect_list)}')

def main():
    max_episodes = 500
    epsilon = 1  # Epsilon-greedy algorithm in initialized at 1 meaning every step is random at the start
    max_epsilon = 1  # You can't explore more than 100% of the time
    min_epsilon = 0.01  # At a minimum, we'll always explore 1% of the time
    decay = 0.01

    render = True
    model = build_model(env.observation_space.sample().shape[0], env.action_space.n)
    # Target model, update every 100 steps
    target_model = build_model(env.observation_space.sample().shape[0], env.action_space.n)
    target_model.set_weights(model.get_weights())

    replay_memory = ReplayMemory(50000)

    target_update_counter = 0

    X = []
    y = []

    steps = 0
    for episode in range(max_episodes):
        total_training_reward = 0
        observation = env.reset(seed=np.random.randint(0, 500000))
        done = False

        while not done:
            steps += 1
            if render:
                env.render()

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

        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay * episode)

    print('Finish Training. Saving Model...')
    target_model.save_weights('my_dqn_weight.h5', overwrite=True)
if __name__ == '__main__':
    test()

