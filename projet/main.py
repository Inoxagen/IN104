#!/usr/bin/env python3

from simulator import Simulator, World, Body
from simulator.utils.vector import Vector2
from simulator.solvers import DummySolver
from simulator.physics.engine import SimpleAvecCollisonEngine
from simulator.physics.engine import SimpleSansCollisonEngine
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
    Soleil = Body(Vector2(0, 0),
              velocity=Vector2(0, 0),
              mass=10,
              color=(255,255,7),
              draw_radius=10)
    Terre = Body(Vector2(0, -1),
              velocity=Vector2(-0.2,0),
              mass=1,
              color=(255,148,23),
              draw_radius=5)

    Mars = Body(Vector2(0, 1),
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
    systeme_solaire = World("Système Solaire",0.1,(0,0,40),10)
    systeme_solaire.add_set([Soleil,Terre,Mars])

    # Set Collision
    monde_pour_collision = World("Monde pour collision",0.1,(0,0,70))
    monde_pour_collision.add_set([b4,b5,b6])

    # Set Aléatoire
    monde_aléatoire = World("Monde aléatoire",0.1,(10,0,0),10,50)
    monde_aléatoire.add_N_corps_aleat_diff(10,[[-4,4],[-4,4]],[[0,0],[0,0]],10)



    # Set Aléatoire Gigantesque
    monde_aléatoire_geant = World("Monde aléatoire gigantesque",2,(0,0,0),10,20) # Petite camera scale
    monde_aléatoire_geant.add_N_corps_aleat_diff(15,[[-20,20],[-20,20]],[[-0.2,0.2],[-0.2,0.2]],100)


    # Choix des monde :
    mondes_simulés=[systeme_solaire,monde_pour_collision,monde_aléatoire,monde_aléatoire_geant]
    mondes_simulés=[monde_aléatoire_geant]
    print("Start program")
    for world in mondes_simulés :
        simulator = Simulator(world, SimpleAvecCollisonEngine, DummySolver)

        screen_size = Vector2(800, 600)
        screen = Screen(screen_size,
                        bg_color=world.bg_color,
                        caption="Simulator")
        screen.camera.scale = world.camera_scale_initial

        # this coefficient controls the speed
        # of the simulation
        time_scale = world.time_scale

        print("  ",world.nom,"avec",len(world),"corps.")
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

            for button in screen._buttons[:5] :
                if button==True :
                    for body in world._bodies:
                        if body.mass!=0 :
                            if (screen.mouse_position-screen.camera.to_screen_coords(body.position)).norm()<=body.draw_radius:
                                screen.camera.position=body.position
                        else:
                            champion=world._bodies[0]
                            for other_body in world._bodies[1:]:
                                if other_body.mass!=0 and (other_body.position-body.position).norm()<(champion.position-body.position).norm():
                                    champion=other_body

                            screen.camera.position=m

            # draw additional stuff
            screen.draw_corner_text("Time: %f" % simulator.t)

            # show new state
            screen.update()

        screen.close()
        print("      Fin de la simulation du",world.nom)
