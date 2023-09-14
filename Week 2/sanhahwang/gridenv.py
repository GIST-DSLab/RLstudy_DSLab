import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces

from IPython import display 
import matplotlib.pyplot as plt


class GridWorldEnv(gym.Env):
  metadata = {"render_modes" : ["human", "rgb_array", "ansi"], "render_fps":4}

  def __init__(self, render_mode = None, size = 5):
    self.size = size
    
    self.observation_space = spaces.Dict(
    {
      "agent": spaces.Box(0, size - 1, shape=(2,), dtype=int),
      "target": spaces.Box(0, size - 1, shape=(2,), dtype=int),
    }
    )
    self.window_size = 512

    self.action_space = spaces.Discrete(4)

    self.action_direction = {
      0 : np.array([0,1]), # up
      1 : np.array([0,-1]), # down
      2 : np.array([1,0]), # right
      3 : np.array([-1,0]), # left 
    }
    self.window = None
    self.clock = None
    
    self.render_mode = render_mode

  def _get_obs(self):
    return {"agent": self._agent_location , "target": self._target_location}

  def _get_info(self):
    return {
      "distance": np.square((self._agent_location - self._target_location)**2)
    }

  def reset(self, seed=None, options=None):
    super().reset(seed=seed)

    self._agent_location = self.np_random.integers(0, self.size, size =2 , dtype=int)
    self. _target_location = self._agent_location

    observation = self._get_obs()
    info = self._get_info()

    return observation, info

  def step(self, action):
    direction = self.action_direction[action]

    self._agent_location = np.clip(
      self._agent_location + direction, 0, self.size - 1
      )

    terminated = np.array_equal(self._agent_location, self._target_location)

    reward = 1 if terminated else 0
    observation = self._get_obs()
    info = self._get_info()



    return observation, reward, terminated, False , info


  
  def render(self):
      if self.render_mode == "rgb_array":
          return self._render_frame()

  def _render_frame(self):
      if self.window is None and self.render_mode == "human":
          pygame.init()
          pygame.display.init()
          self.window = pygame.display.set_mode(
              (self.window_size, self.window_size)
          )
      if self.clock is None and self.render_mode == "human":
          self.clock = pygame.time.Clock()

      canvas = pygame.Surface((self.window_size, self.window_size))
      canvas.fill((255, 255, 255))
      pix_square_size = (
          self.window_size / self.size
      )  # The size of a single grid square in pixels

      # First we draw the target
      pygame.draw.rect(
          canvas,
          (255, 0, 0),
          pygame.Rect(
              pix_square_size * self._target_location,
              (pix_square_size, pix_square_size),
          ),
      )
      # Now we draw the agent
      pygame.draw.circle(
          canvas,
          (0, 0, 255),
          (self._agent_location + 0.5) * pix_square_size,
          pix_square_size / 3,
      )

      # Finally, add some gridlines
      for x in range(self.size + 1):
          pygame.draw.line(
              canvas,
              0,
              (0, pix_square_size * x),
              (self.window_size, pix_square_size * x),
              width=3,
          )
          pygame.draw.line(
              canvas,
              0,
              (pix_square_size * x, 0),
              (pix_square_size * x, self.window_size),
              width=3,
          )

      if self.render_mode == "human":
          # The following line copies our drawings from `canvas` to the visible window
          self.window.blit(canvas, canvas.get_rect())
          pygame.event.pump()
          pygame.display.update()

          # We need to ensure that human-rendering occurs at the predefined framerate.
          # The following line will automatically add a delay to keep the framerate stable.
          self.clock.tick(self.metadata["render_fps"])
      else:  # rgb_array
          return np.transpose(
              np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
          )
  def close(self):
      if self.window is not None:
          pygame.display.quit()
          pygame.quit()
