from .vector import Vector2
from ..utils.uid import UID

import random as rd
import math


class Body:
    def __init__(self, position, velocity=Vector2(0, 0), mass=1, color=(255, 255, 255), draw_radius=50,nom=""):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.color = color
        self.draw_radius = draw_radius
        self.nom=nom

    def __str__(self):
        return "%s position:%s, vitesse:%s, masse:%.2f" % (self.nom, self.position, self.velocity, self.mass)


class World:
    def __init__(self, nom="", modeParlant=True, seuil_collision=0, bg_color=(0,0,0), time_scale=10, camera_scale_initial=50):
        self._bodies = []
        self.total_corps=0 # Comptabilise le nombre de corps vivant et ayant vécu.
        self.nom=nom
        self.modeParlant=modeParlant
        self.seuil_collision=seuil_collision
        self.bg_color=bg_color
        self.time_scale=time_scale
        self.camera_scale_initial=camera_scale_initial

    def add(self, body):
        """ Add `body` to the world.
            Return a unique ID for `body`.
        """
        new_id = len(self._bodies)
        self._bodies.append(body)
        self.total_corps+=1
        return new_id

    def add_set(self, liste_de_corps):
        """ Pour ajouter une liste de corps"""
        list_id=[]
        for body in liste_de_corps :
            list_id.append(self.add(body))
        return list_id

    def add_N_corps_aleat_diff(self,N, borne_pos, borne_vit, mass_max):
        """" Ajoute des corps aléatoires a des positions differentes """

        # Récupération des positions déjà occupées
        list_pos_occupées=[]
        for corps in self._bodies:
            list_pos_occupées.append([corps.position.get_x,corps.position.get_y])

        # Aléatoire -> Nouvelles positions
        list_pos_vide_aleat=[]
        L=len(borne_pos)
        for i in range(N):
            ele_aleat=[borne_pos[i][0]+rd.random()*(borne_pos[i][1]-borne_pos[i][0]) for i in range(L)]
            while(ele_aleat in list_pos_occupées+list_pos_vide_aleat):
                ele_aleat=[borne_pos[i][0]+rd.random()*(borne_pos[i][1]-borne_pos[i][0]) for i in range(L)]
            list_pos_vide_aleat.append(ele_aleat) # On l'ajoute au position aléatoire

        # Aléatoire -> Toutes les autres paramètres des corps
        list_id=[]
        for pos in list_pos_vide_aleat :
            mass=rd.random()*mass_max

            b_aleat = Body(Vector2(pos[0], pos[1]),
                    velocity=Vector2(borne_vit[0][0]+rd.random()*(borne_vit[0][1]-borne_vit[0][0]),
                                     borne_vit[1][0]+rd.random()*(borne_vit[1][1]-borne_vit[1][0])),
                    mass=mass,
                    color=tuple([rd.randint(0,255) for i in range(3)]),
                    draw_radius=4*mass/mass_max*int(math.log(mass+1))+1,
                    nom=str(rd.randbytes(1))) # Des beaux noms d'astréroïdes

            list_id.append(self.add(b_aleat)) # On ajoute le nouveau corps et on stoque son id pour le renvoyer
        return list_id

    def clear_all(self,seuil_collision=-1, bg_color=(-1,-1,-1)):
        """ Supprime tout les corps,
        possibilité de redefinir le seuil et la couleur """
        self._bodies = []
        if seuil_collision!=-1 :
            self.seuil_collision=seuil_collision
        if bg_color!=(-1,-1,-1):
            self.bg_color=bg_color
        return None

    def pop(self, index):
        """ Supprime l'élément d'index 'index' du monde.
            Return le `body` supprimé.
        """
        return self._bodies.pop(index)

    def get(self, id_):
        """ Return the body with ID `id`.
            If no such body exists, return None.
        """
        if (id_ >= 0 and id_ < len(self._bodies)):
            return self._bodies[id_]
        return None

    def bodies(self):
        """ Return a generator of all the bodies. """
        for body in self._bodies:
            yield body

    def __len__(self):
        """ Return the number of bodies """
        return len(self._bodies)

    def __str__(self):
        return "Bodies: %d\n\t%s" % \
            (len(self),
             '\n\t'.join([str(i) + ": " + str(self._bodies[i])
                          for i in range(len(self))]))
