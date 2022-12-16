from gym.envs.registration import register

# Remeber to change 'GridWorldEnv' in entry_point and also the id name
register(
    id="car_racing/env_main",
    entry_point="car_racing.envs:GridWorldEnv",
)