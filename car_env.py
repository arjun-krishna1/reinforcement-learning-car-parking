import gym
from gym import spaces
import numpy as np
import time
import csv
from math import sqrt, pow, pi

import pymunk

import matplotlib.pyplot as plt

from Reader import Case

SPEED = 1
ANGULAR_SPEED = 0.1
TURN_THRESHOLD = 0.7

colliding = False

class CarEnv(gym.Env):
    """Environment for car path planning"""

    metadata = {"render.modes": ["human"]}

    def __init__(self, draw: bool) -> None:
        super(CarEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        # move left, up, right or down; rotate CCW or CW
        # self.action_space = spaces.Discrete(6)
        self.action_space = spaces.Discrete(4) # TODO add angle back in
        # Example for using image as input (channel-first; channel-last also works):
        #(delta_x, delta_y, delta_theta), distance to locatoin
        self.observation_space = spaces.Box(
            low=-10000, high=10000, shape=(3,), dtype=np.float64
        )
        
        self.draw = draw
        self.last_dist = float('inf')

        i = 19
        self.case  = Case.read('BenchmarkCases/Case%d.csv' % (i + 1))

        self.car_x = self.case.x0
        self.car_y = self.case.y0
        self.car_theta = self.case.theta0

        self.space = pymunk.Space()

        if self.draw:
            plt.ion()
            self.fig = plt.figure()
            plt.xlim(self.case.xmin, self.case.xmax)
            plt.ylim(self.case.ymin, self.case.ymax)
            plt.gca().set_aspect('equal', adjustable = 'box')
            plt.gca().set_axisbelow(True)
            plt.title('self.case %d' % (i + 1))
            plt.grid(linewidth = 0.2)
            plt.xlabel('X / m', fontsize = 14)
            plt.ylabel('Y / m', fontsize = 14)

            for j in range(0, self.case.obs_num):
                plt.fill(self.case.obs[j][:, 0], self.case.obs[j][:, 1], facecolor = 'k', alpha = 0.5)
                obs_body = pymunk.Body()
                obs_body.position = pymunk.Vec2d()
                
                obs_shape = pymunk.Poly(obs_body, self.case.obs[j])
                obs_shape.collision_type = 1
                # detect collisions but don't affect movement of car
                obs_shape.sensor = True
                self.space.add(obs_body, obs_shape)
            
            plt.arrow(self.case.x0, self.case.y0, np.cos(self.case.theta0), np.sin(self.case.theta0), width=0.2, color = "gold")
            plt.arrow(self.case.xf, self.case.yf, np.cos(self.case.thetaf), np.sin(self.case.thetaf), width=0.2, color = "gold")
            temp = self.case.vehicle.create_polygon(self.case.x0, self.case.y0, self.case.theta0)
            plt.plot(temp[:, 0], temp[:, 1], linestyle='--', linewidth = 0.4, color = 'green')
            
            # set up car for physics engine
            car_body = pymunk.Body()
            # set the car body position as the center of real axle
            car_body.position = pymunk.Vec2d(self.case.x0, self.case.y0)
            # TODO rotate car body in pymunk engine

            # set the car's shape
            self.car_shape = pymunk.Poly(car_body, temp)
            self.car_shape.mass = 1
            self.car_shape.collision_type = 0

            self.space.add(car_body, self.car_shape)

            temp = self.case.vehicle.create_polygon(self.case.xf, self.case.yf, self.case.thetaf)
            plt.plot(temp[:, 0], temp[:, 1], linestyle='--', linewidth = 0.4, color = 'red')

        col_handler = self.space.add_collision_handler(0, 1)
        def collide(self, arbiter, space):
            # print('colliding!')
            # TODO what is proper way to set flag in environment when this happens?
            colliding = True
        
        col_handler.begin = collide


    def step(self, action):
        if self.draw:
            temp = self.case.vehicle.create_polygon(self.car_x, self.car_y, self.case.theta0)
            plt.plot(temp[:, 0], temp[:, 1], linestyle='--', linewidth = 0.4, color = 'green')
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

        if action == 0:
            self.car_x -= SPEED
        if action == 1:
            self.car_y += SPEED
        if action == 2:
            self.car_x += SPEED
        if action == 3:
            self.car_y -= SPEED
        # if action == 4:
        #     self.car_theta += ANGULAR_SPEED
        # if action == 5:
        #     self.car_theta -= ANGULAR_SPEED

        dist = sqrt(pow(self.case.xf - self.car_x, 2) + pow(self.case.yf - self.car_y, 2) + pow(self.case.thetaf - self.car_theta, 2))
        
        self.reward = 1 - pow(dist, 0.4)

        COLLIDING_PENALTY = -1

        if colliding:
            self.reward -= COLLIDING_PENALTY

        info = {
            "car_x": self.car_x,
            "car_y": self.car_y,
            "goal_x": self.case.xf,
            "goal_y": self.case.yf,
            "dist": dist,
        }
        observation = self.__get_dist()
        return observation, self.reward, dist == 0, info

    def reset(self):
        self.car_x = self.case.x0
        self.car_y = self.case.y0

        observation = self.__get_dist()
        return observation
    
    def close(self):
        plt.close(self.fig)
    
    def __get_dist(self):
        return np.array([self.case.xf - self.car_x, self.case.yf - self.car_y, self.case.thetaf - self.car_theta])

