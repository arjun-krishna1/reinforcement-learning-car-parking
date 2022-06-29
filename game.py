
'''
Adapted from
https://github.com/CapAI/ship-sim-gym
'''
from .Reader import Case


SPEED = 10

class CarParkGame(object):

    car = None
    obstacles = list()

    frame_counter = 0
    base_dt = 0.1
    colliding = False

    def __init__(self, draw: bool) -> None:

        # number of dt's to skip each step
        self.speed = 10
        self.fps = 1000
        self.bounds = 
        self.screen = pygame.display.set_mode()
        self.clock = pygame.time.Clock()
        self.goal_reached = False
        self.colliding = False
        self.draw = draw

        if draw:
            pygame.init()
            pygame.display.set_caption("Car Park Gym")
            pygame.key.set_repeat(10, 10)
        
        print("CAR PARK SIM STARTED")
        self.reset()
    
    def read_case(self, number: int) -> None
        """
        Read case from csv
        """
        # TODO throw better error if case doesn't exist
        case = Case.read("BenchmarkCases/Case%d.csv" % (number + 1))

        self.case = case

        # car's initial position
        self.car_x = self.case.x0
        self.car_y = self.case.y0
        self.car_theta = self.case.theta0

    def step(self, action: int):
                if action == 0:
            self.car_x -= SPEED
        if action == 1:
            self.car_y += SPEED
        if action == 2:
            self.car_x += SPEED
        if action == 3:
            self.car_y -= SPEED
        if action == 4:
            self.car_theta += ANGULAR_SPEED
        if action == 5:
            self.car_theta -= ANGULAR_SPEED
        if self.draw:
            # TODO draw do pygame stuff here

        

