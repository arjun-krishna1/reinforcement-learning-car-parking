import gym
from gym import spaces
import numpy as np
import time
import csv
from math import sqrt, pow

import matplotlib.pyplot as plt


class Vehicle:
    def __init__(self):
        self.lw = 2.8  # wheelbase
        self.lf = 0.96  # front hang length
        self.lr = 0.929  # rear hang length
        self.lb = 1.942  # width

    def create_polygon(self, x, y, theta):
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)

        points = np.array([
            [-self.lr, -self.lb / 2, 1],
            [self.lf + self.lw, -self.lb / 2, 1],
            [self.lf + self.lw, self.lb / 2, 1],
            [-self.lr, self.lb / 2, 1],
            [-self.lr, -self.lb / 2, 1],
        ]).dot(np.array([
            [cos_theta, -sin_theta, x],
            [sin_theta, cos_theta, y],
            [0, 0, 1]
        ]).transpose())
        return points[:, 0:2]


class Case:
    def __init__(self):
        self.x0, self.y0, self.theta0 = 0, 0, 0
        self.xf, self.yf, self.thetaf = 0, 0, 0
        self.xmin, self.xmax = 0, 0
        self.ymin, self.ymax = 0, 0
        self.obs_num = 0
        self.obs = np.array([])
        self.vehicle = Vehicle()

    @staticmethod
    def read(file):
        case = Case()
        with open(file, 'r') as f:
            reader = csv.reader(f)
            tmp = list(reader)
            v = [float(i) for i in tmp[0]]
            case.x0, case.y0, case.theta0 = v[0:3]
            case.xf, case.yf, case.thetaf = v[3:6]
            case.xmin = min(case.x0, case.xf) - 8
            case.xmax = max(case.x0, case.xf) + 8
            case.ymin = min(case.y0, case.yf) - 8
            case.ymax = max(case.y0, case.yf) + 8

            case.obs_num = int(v[6])
            num_vertexes = np.array(v[7:7 + case.obs_num], dtype=np.int)
            vertex_start = 7 + case.obs_num + (np.cumsum(num_vertexes, dtype=np.int) - num_vertexes) * 2
            case.obs = []
            for vs, nv in zip(vertex_start, num_vertexes):
                case.obs.append(np.array(v[vs:vs + nv * 2]).reshape((nv, 2), order='A'))
        return case

INIT_CAR_X = 200
INIT_CAR_Y = 200

GOAL_X = 700
GOAL_Y = 500

SPEED = 1

class CarEnv(gym.Env):
    """Environment for car path planning"""

    metadata = {"render.modes": ["human"]}

    def __init__(self, draw: bool) -> None:
        super(CarEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        # move left, up, right or down
        self.action_space = spaces.Discrete(4)
        # Example for using image as input (channel-first; channel-last also works):
        #(delta_x, delta_y), distance to locatoin
        self.observation_space = spaces.Box(
            low=-10000, high=10000, shape=(2,), dtype=np.float64
        )
        
        self.draw = draw

        i = 0
        self.case  = Case.read('BenchmarkCases/Case%d.csv' % (i + 1))

        self.car_x = self.case.x0
        self.car_y = self.case.y0
        self.car_theta = self.case.theta0

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

        dist = sqrt(pow(GOAL_X - self.car_x, 2) + pow(GOAL_Y - self.car_y, 2))
        MAX_REWARD = 100000
        if dist == 0:
            reward = MAX_REWARD
        else:
            reward = 1 / dist

        self.reward = reward

        info = {}
        observation = self.__get_dist()
        return observation, reward, reward == MAX_REWARD, info

    def reset(self):
        self.car_x = self.case.x0
        self.car_y = self.case.y0

        observation = self.__get_dist()
        return observation
    
    def __get_dist(self):
        return np.array([GOAL_X - self.car_x, GOAL_Y - self.car_y])

