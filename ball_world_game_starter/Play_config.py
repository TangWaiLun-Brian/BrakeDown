import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--episode', type=int, default=1)
parser.add_argument('--seed', type=int, default=1)

parser.add_argument('--num_of_obs', type=int, default=10)
parser.add_argument('--num_of_br', type=int, default=5)
parser.add_argument('--num_of_acc', type=int, default=1)
parser.add_argument('--ball_initial_speed', type=float, default=6.)
parser.add_argument('--num_of_accelerator', type=int, default=1)

parser.add_argument('--fps', type=int, default=60)
parser.add_argument('--mode', type=str, choices=['human', 'human_rand'], default='human')
parser.add_argument('-v', action='store_true')

args = parser.parse_args()