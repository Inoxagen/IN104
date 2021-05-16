#!/usr/bin/env python3

from simulator import Simulator, World, Body
from simulator.utils.vector import Vector2
from simulator.solvers import DummySolver
from simulator.physics.engine import DummyPlusCollisonEngine
from simulator.graphics import Screen

import pygame as pg

"""def egalite_liste(L1,L2):
    if len(L1)!=len(L2):    return False
    for i in range(len(L1)):
        if L1[i]!=L2[i]:    return False
    return True

def list_ent_aleat_diff(nbre_de_tuplet,longueur,list_val_min_max):
    # liste entier aleatoire different
    list_retour=[]
    for i in range(nbre_de_tuplet):
        ele_aleat=[list_val_min_max[i][0]+rd.random()*(list_val_min_max[i][1]-list_val_min_max[i][0]) for i in range(longueur)]
        while(ele_aleat in list_retour):
            ele_aleat=[list_val_min_max[i][0]+rd.random()*(list_val_min_max[i][1]-list_val_min_max[i][0]) for i in range(longueur)]
        list_retour.append(ele_aleat)
    return list_retour

def N_corps_aleat_diff(N, borne_pos, borne_vit, mass_max):
    # Créee une liste de corps aléatoires a des positions differentes
    # resol pas du hasard
    list_corps=[]

    list_pos=list_ent_aleat_diff(N,len(borne_pos),borne_pos,resol)
    for pos in list_pos:
        mass=rd.random()*mass_max

        b_aleat = Body(Vector2(pos[0], pos[1]),
                velocity=Vector2(borne_vit[0][0]+rd.random()*(borne_vit[0][1]-borne_vit[0][0]), borne_vit[1][0]+rd.random()*(borne_vit[1][1]-borne_vit[1][0])),
                mass=mass,
                color=tuple([rd.randint(0,255) for i in range(3)]),
                draw_radius=int(5*math.log(mass)))
        list_corps.append(b_aleat)

    return list_corps
"""



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
    b6 = Body(Vector2(0, 5),
              velocity=Vector2(0,0),
              mass=3,
              color=(0,0,255),
              draw_radius=5)


    # Set Soleil Terre Mars
    systemeSolaire = World(0.1,(0,0,40))
    systemeSolaire.add_set([b1,b2,b3])

    # Set Collision
    #world.add_set([b4,b5,b6])

    # Set Aléatoire
    world=World(100,(0,0,40))
    world.add_N_corps_aleat_diff(10,[[-1000,1000],[-1000,1000]],[[-2,2],[-2,2]],1000)

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
