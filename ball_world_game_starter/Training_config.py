import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--episode', type=int, default=200)
parser.add_argument('--batch_size', type=int, default=64)
parser.add_argument('--train_step', type=int, default=4)
parser.add_argument('--update_step', type=int, default=100)
parser.add_argument('--learning_rate', type=float, default=0.7)
parser.add_argument('--discount_factor', type=float, default=0.62)
parser.add_argument('--replay_size', type=int, default=100000)
parser.add_argument('--max_epsilon', type=float, default=1.)
parser.add_argument('--min_epsilon', type=float, default=0.01)
parser.add_argument('--decay_rate', type=float, default=0.01)

parser.add_argument('--seed', type=int, default=1)
parser.add_argument('--num_of_obs', type=int, default=10)
parser.add_argument('--num_of_br', type=int, default=5)
parser.add_argument('--num_of_acc', type=int, default=1)
parser.add_argument('--ball_initial_speed', type=float, default=3.)
parser.add_argument('--num_of_accelerator', type=int, default=1)

parser.add_argument('--fps', type=int, default=120)
parser.add_argument('--mode', type=str, choices=['train'], default='train')
parser.add_argument('-v', action='store_true')
parser.add_argument('--save_model', type=bool, default=True)
# Setting to the third model name to avoid over-written the pretrained models
parser.add_argument('--model_name', type=str, default='my_dqn_weight_3.h5')

args = parser.parse_args()