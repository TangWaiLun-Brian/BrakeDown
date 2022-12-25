from gym.envs.registration import register

# Remeber to change 'GridWorldEnv' in entry_point and also the id name
register(
    id="ball_world_game/env_main-v0",
    entry_point="ball_world_game.envs:CustomEnv",
)
