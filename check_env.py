from stable_baselines3.common.env_checker import check_env
from car_env import CarEnv

from time import sleep

env = CarEnv()

check_env(env)

episodes = 50

for episode in range(episodes):
	done = False
	obs = env.reset()
	while True:
		random_action = env.action_space.sample()
		print("action",random_action)
		obs, reward, done, info = env.step(random_action)
		print('reward',reward)
