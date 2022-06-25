"""Port of the Chipmunk tank demo. Showcase a topdown tank driving towards the
mouse, and hitting obstacles on the way.
"""

import random

import pygame

import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d


def update(space, dt, surface):
    global tank_body
    global tank_control_body

    direction = 5.0
    dv = Vec2d(direction, 0.0)
    tank_control_body.velocity = tank_body.rotation_vector.cpvrotate(dv)
    print(tank_control_body.position)
    space.step(dt)


def add_car_body(space, size, mass):

    body = pymunk.Body(1,  float("inf"))
    space.add(body)

    radius = 5
    # TODO update so position is average x and average y o fthe car's position
    body.position = Vec2d(0, 0)

    shape = pymunk.Poly.create_box(body, (size, size), 0.0)
    shape.mass = mass
    space.add(shape)

    return body

def add_obs_body(space, vertices):
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    # what should body of a n polygon be?
    # average x and y?
    body.position = sum(
        [v[0] for v in vertices]) / len(vertices), sum(
        [v[1] for v in vertices]) / len(vertices)

    shape = pymunk.Poly(body, vertices)
    shape.color = pygame.Color("blue")
    shape.group = 1
    space.add(body, shape)

def init():

    space = pymunk.Space()
    space.iterations = 10
    space.sleep_time_threshold = 0.5

    # We joint the tank to the control body and control the tank indirectly by modifying the control body.
    global tank_control_body
    tank_control_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    tank_control_body.position = 20, 20
    space.add(tank_control_body)
    global tank_body
    tank_body = add_car_body(space, 30, 10)
    tank_body.position = 20, 20
    for s in tank_body.shapes:
        s.color = (0, 255, 100, 255)

    pivot = pymunk.PivotJoint(tank_control_body, tank_body, (0, 0), (0, 0))
    space.add(pivot)
    pivot.max_bias = 0  # disable joint correction
    pivot.max_force = 10000  # emulate linear friction

    gear = pymunk.GearJoint(tank_control_body, tank_body, 0.0, 1.0)
    space.add(gear)
    gear.error_bias = 0  # attempt to fully correct the joint each step
    gear.max_bias = 1.2  # but limit it's angular correction rate
    gear.max_force = 50000  # emulate angular friction

    add_obs_body(space, [[50, -100], [100, -100], [100, 0], [50, 0], ])

    return space


space = init()
pygame.init()
screen = pygame.display.set_mode((1280, 960))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

while True:
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN
            and (event.key in [pygame.K_ESCAPE, pygame.K_q])
        ):
            exit()

    screen.fill(pygame.Color("black"))
    space.debug_draw(draw_options)
    fps = 60
    update(space, 1 / fps, screen)
    pygame.display.flip()

    clock.tick(fps)
