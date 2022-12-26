import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--episode', type=int, default=10)

parser.add_argument('--seed', type=int, default=1)
parser.add_argument('--num_of_obs', type=int, default=10)
parser.add_argument('--num_of_br', type=int, default=5)
parser.add_argument('--num_of_acc', type=int, default=1)
parser.add_argument('--ball_initial_speed', type=float, default=3.)

parser.add_argument('--fps', type=int, default=120)
parser.add_argument('--mode', type=str, choices=['test'], default='test')
parser.add_argument('-v', action='store_true')
# Our current model is 'my_dqn_weight_2.h5'
parser.add_argument('--model_name', type=str, default='my_dqn_weight_2.h5')

args = parser.parse_args()