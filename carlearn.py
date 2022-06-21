import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.logger import TensorBoardOutputFormat

from car_env import CarEnv

import os
import time

class SummaryWriterCallback(BaseCallback):
	'''
	Snippet skeleton from Stable baselines3 documentation here:
	https://stable-baselines3.readthedocs.io/en/master/guide/tensorboard.html#directly-accessing-the-summary-writer
	'''

	def _on_training_start(self):
		self._log_freq = 10  # log every 10 calls

		output_formats = self.logger.output_formats
		# Save reference to tensorboard formatter object
		# note: the failure case (not formatter found) is not handled here, should be done with try/except.
		self.tb_formatter = next(formatter for formatter in output_formats if isinstance(formatter, TensorBoardOutputFormat))

	def _on_step(self) -> bool:
		'''
		Log my_custom_reward every _log_freq(th) to tensorboard for each environment
		'''
		if self.n_calls % self._log_freq == 0:
			self.tb_formatter.writer.add_scalar("rewards/env #1",
													self.locals["rewards"][0],
													self.n_calls)

if __name__ == "__main__":
	models_dir = f"models/{int(time.time())}/"
	logdir = f"logs/{int(time.time())}/"

	if not os.path.exists(models_dir):
		os.makedirs(models_dir)

	if not os.path.exists(logdir):
		os.makedirs(logdir)

	env = CarEnv(draw=False)
	env.reset()

	model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

	TIMESTEPS = 100000
	iters = 0
	while True:
		iters += 1
		model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO", callback=SummaryWriterCallback())
		model.save(f"{models_dir}/{TIMESTEPS*iters}")
