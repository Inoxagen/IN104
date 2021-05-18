#!/usr/bin/env python3

from simulator import Simulator, World, Body
from simulator.utils.vector import Vector2
from simulator.solvers import DummySolver
from simulator.physics.engine import SimpleAvecCollisonEngine
from simulator.physics.engine import SimpleSansCollisonEngine
from simulator.graphics import Screen

import pygame as pg
import random as rd

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
    monde_aléatoire_geant.add_N_corps_aleat_diff(17,[[-20,20],[-20,20]],[[-0.2,0.2],[-0.2,0.2]],100)


    # Choix des monde :
    mondes_simulés=[systeme_solaire,monde_pour_collision,monde_aléatoire,monde_aléatoire_geant]
    #mondes_simulés=[monde_aléatoire_geant]
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

            # draw current state
            screen.draw(world)

            dt = screen.tick(60)

            # -Barre espace (-> pause simulation)
            if not screen.get_space_key():
                # simulate physics
                delta_time = time_scale * dt / 1000
                simulator.step(delta_time)


            # Nettoyage des objets de masse nulle
            a_retirer=[]
            for i in range(len(world)):
                if world._bodies[i].mass==0:
                    a_retirer=[i]+a_retirer #Ajout au début
            for i in a_retirer:
                b_pop=world.pop(i)
                print("      X> Suppression de :",i)
                if i==screen.camera.id_ref:
                    # Si la masse du corps de reference est nul
                    # possiblement après une collision,
                    # on cherche le corps le plus proche que l'on suivra a son tour
                    print("     ?> Recherche plus proche de ",i)
                    id_champ=i # On retire toujours l'indice le plus petit.
                    b_champion=world._bodies[i]
                    for j in range(i+1,len(world)):
                        b_test=world._bodies[j]
                        if (b_test.mass!=0 and (b_test.position-b_pop.position).norm()<(b_champion.position-b_pop.position).norm()) or b_champion.mass==0 :
                            #Si la masse du champion est nulle on change de champion
                            id_champ=j
                            b_champion=world._bodies[id_champ]
                    screen.camera.id_ref=id_champ
                    print("     O> Trouvé en :",id_champ," (ex:",id_champ+1,")")

                elif i<screen.camera.id_ref:
                    screen.camera.id_ref-=1
            if len(a_retirer)!=0:
                a_retirer=[]
                simulator.re_init(world) # On refait l'initialisation de la simulation


            # Lecture des Evenements
            screen.get_events()

            # Conséquences des évènements :
            # -Evenement clavier
            if screen._buttons[7]==True:
                screen.camera.position[1]+=5/screen.camera.scale
            if screen._buttons[5]==True:
                screen.camera.position[0]+=5/screen.camera.scale
            if screen._buttons[8]==True:
                screen.camera.position[1]-=5/screen.camera.scale
            if screen._buttons[6]==True:
                screen.camera.position[0]-=5/screen.camera.scale

            # -Molette souris (zoom camera)
            if screen.get_wheel_up():
                screen.camera.scale *= 1.1
            elif screen.get_wheel_down():
                screen.camera.scale *= 0.9

            # -Clic central souris (déplacement camera)
            if screen.get_middle_mouse():
                screen.camera.id_ref=-1
                screen.camera.position+=screen.camera.scale*(screen.mouse_position-screen_size/2)/100000

            # -Clic gauche (focalisation/fixation camera)
            if screen.get_left_mouse():
                screen.camera.id_ref=-1
                for i in range(len(world)):
                    body = world._bodies[i]
                    if body.mass!=0 :
                        if (screen.mouse_position-screen.camera.to_screen_coords(body.position)).norm()<=body.draw_radius:
                            screen.camera.id_ref=i
                screen.camera.position=screen.camera.from_screen_coords(screen.mouse_position)

            if screen.camera.id_ref!=-1:
                # On suit le corps referent
                screen.camera.position=world._bodies[screen.camera.id_ref].position

            # -Clic droit
            if screen.get_right_mouse():
                world.add(Body(screen.camera.from_screen_coords(screen.mouse_position),
                            velocity=Vector2(0,0),
                            mass=1,
                            color=tuple([rd.randint(0,255) for i in range(3)]),
                            draw_radius=1))
                simulator.re_init(world) # On refait l'initialisation de la simulation


            # draw additional stuff
            screen.draw_corner_text("Corps restant : "+str(len(world))+"/"+str(world.total_corps)+"  ---  Time: %f" % simulator.t)

            # show new state
            screen.update()

        screen.close()
        print("      Fin de la simulation du",world.nom)
