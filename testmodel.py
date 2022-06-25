import gym
from stable_baselines3 import PPO
from car_env import CarEnv

models_dir = "models"
model_path = "models/1655764236/400000.zip"


env = CarEnv(draw=True, benchmark_num=2)
env.reset()
model = PPO.load(model_path, env=env)

EPISODES = 5


for ep in range(EPISODES):
    obs = env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        print(info["dist"])
