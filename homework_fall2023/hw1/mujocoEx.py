import random
from gym.envs.mujoco.ant_v4 import AntEnv
env = AntEnv()

for _ in range(10000):
	env.render()
	action = [random.randint(0,1) for _ in range(env.action_space.shape[0])]
	_, _, _, _ = env.step(action)

env.close()