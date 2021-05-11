#!/usr/bin/env python3

from simulator import Simulator, World, Body
from simulator.utils.vector import Vector2
from simulator.solvers import DummySolver
from simulator.physics.engine import DummyPlusCollisonEngine
from simulator.graphics import Screen

import pygame as pg

if __name__ == "__main__":
    b1 = Body(Vector2(0, 0),
              velocity=Vector2(0, 0),
              mass=10,
              color=(255,255,7),
              draw_radius=10)
    b2 = Body(Vector2(0, -1),
              velocity=Vector2(-0.2,0),
              mass=1,
              color=(255,148,23),
              draw_radius=5)

    b3 = Body(Vector2(0, 1),
              velocity=Vector2(0.2,0),
              mass=1,
              color=(9,156,237),
              draw_radius=5)
    # Pour Collision
    b4 = Body(Vector2(0, -1),
              velocity=Vector2(0, 0),
              mass=1,
              color=(255,0,0),
              draw_radius=5)
    b5 = Body(Vector2(0, 1),
              velocity=Vector2(0,0),
              mass=1,
              color=(0,255,0),
              draw_radius=5)
    b6 = Body(Vector2(0, 10),
              velocity=Vector2(0,0),
              mass=1,
              color=(0,0,255),
              draw_radius=5)

    world = World(0.05,(0,0,40))
    #world.add(b1)
    #world.add(b2)
    #world.add(b3)
    world.add(b4)
    world.add(b5)
    world.add(b6)

    simulator = Simulator(world, DummyPlusCollisonEngine, DummySolver)

    screen_size = Vector2(800, 600)
    screen = Screen(screen_size,
                    bg_color=world.bg_color,
                    caption="Simulator")
    screen.camera.scale = 50

    # this coefficient controls the speed
    # of the simulation
    time_scale = 10

    print("Start program")
    while not screen.should_quit:
        dt = screen.tick(60)

        # simulate physics
        delta_time = time_scale * dt / 1000
        simulator.step(delta_time)

        # read events
        screen.get_events()

        # handle events
        #   scroll wheel
        if screen.get_wheel_up():
            screen.camera.scale *= 1.1
        elif screen.get_wheel_down():
            screen.camera.scale *= 0.9

        # draw current state
        screen.draw(world)

        # draw additional stuff
        screen.draw_corner_text("Time: %f" % simulator.t)

        # show new state
        screen.update()

    screen.close()
    print("Done")
