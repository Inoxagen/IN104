from ..utils.vector import Vector, Vector2
from .constants import G


def gravitational_force(pos1, mass1, pos2, mass2):
    """ Return the force applied to a body in pos1 with mass1
        by a body in pos2 with mass2
    """
    vecteur_difference=pos1-pos2
    d=Vector.norm(vecteur_difference)
    if d!=0 :
        # Force de A sur B = G* mA * mB / d² dans la direction A vers B
        return (-G*mass1*mass2/(d*d*d))*vecteur_difference
    else:
        return Vector(len(pos1))  #  Vecteur nul bonne longueur


def force_grav_massiq_depuis_diff(vecteur_difference):
    """ La difference est calculée pour vérifier les colisions
        La masse 1 etait passée à 1 pour éviter de diviser
        -> on les retire des paramètres
    """
    d=Vector.norm(vecteur_difference)
    # Force de A sur B = G* mA * mB / d² dans la direction A vers B
    return (-G/(d*d*d))*vecteur_difference


class IEngine:
    def __init__(self, world):
        self.world = world
        self.n=len(self.world)
        if self.n>0 :
            self.dim=len(self.world._bodies[0].position)

    def derivatives(self, t0, y0):
        """ This is the method that will be fed to the solver
            it does not use it's first argument t0,
            its second argument y0 is a vector containing the positions
            and velocities of the bodies, it is laid out as follow
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.

            Return the derivative of the state, it is laid out as follow
                [vx1, vy1, vx2, vy2, ..., vxn, vyn, ax1, ay1, ax2, ay2, ..., axn, ayn]
            where vxi, vyi are the velocities and axi, ayi are the accelerations.
        """

        raise NotImplementedError



    def make_solver_state(self):
        """ Returns the state given to the solver, it is the vector y in
                y' = f(t, y)
            In our case, it is the vector containing the
            positions and speeds of all our bodies:
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.
        """
        raise NotImplementedError



class DummyEngine(IEngine):

    def derivatives(self, t0, y0):
         # [vx1, vy1, vx2, vy2, ..., vxn, vyn]
        y1=Vector(2*self.dim*self.n)

        for i in range(self.n):
            # Vitesse
            y1[self.dim*i]= y0[(self.n + i)*self.dim]
            y1[self.dim*i+1]= y0[(self.n + i)*self.dim+1]

            # Acceleration
            acc_i=Vector2(0,0)
            pos_i=Vector2(y0[self.dim*i],y0[self.dim*i+1])
            # On l'enregistre pour ne pas avoir a l'appeler a chaque fois
            # mass_i=self.world[i].mass Inutile de multiplier par mass_i pour diviser par mass_i juste après

            for j in range(self.n):
                if(i!=j):
                    acc_i+=gravitational_force(pos_i, 1, Vector2(y0[self.dim*j],y0[self.dim*j+1]), self.world._bodies[j].mass)

            y1[self.dim*self.n + self.dim*i ] = acc_i.get_x()
            y1[self.dim*self.n + self.dim*i+1]= acc_i.get_y()

        return y1


    def make_solver_state(self):
        y=Vector(4*self.n)

        for i in range(self.n):
            y[self.dim*i]= self.world._bodies[i].position.get_x()
            y[self.dim*i+1]= self.world._bodies[i].position.get_y()
            y[self.dim*self.n + self.dim*i ] = self.world._bodies[i].velocity.get_x()
            y[self.dim*self.n + self.dim*i+1]= self.world._bodies[i].velocity.get_y()
        return y


class SimpleSansCollisonEngine(DummyEngine):
    def derivatives(self, t0, y0):
        self.n=len(self.world)

        y1=Vector(len(y0)) # Pouur stoquer : [vx1, vy1, vx2, vy2, ..., vxn, vyn]

        vect_acc=Vector2(0,0)  # Acceleration

        for i in range(self.n):
            # Vitesse :
            y1[self.dim*i]= y0[(self.n + i)*self.dim]
            y1[self.dim*i+1]= y0[(self.n + i)*self.dim+1]


            pos_i=Vector2(y0[self.dim*i],y0[self.dim*i+1])

            for j in range(i):
                vect_acc=force_grav_massiq_depuis_diff(pos_i - Vector2(y0[self.dim*j],y0[self.dim*j+1]))
                y1[self.dim*self.n + self.dim*i ] += self.world._bodies[j].mass*vect_acc.get_x()
                y1[self.dim*self.n + self.dim*i+1]+= self.world._bodies[j].mass*vect_acc.get_y()
                y1[self.dim*self.n + self.dim*j ] += -self.world._bodies[i].mass*vect_acc.get_x()
                y1[self.dim*self.n + self.dim*j+1]+= -self.world._bodies[i].mass*vect_acc.get_y()
        return y1


class SimpleAvecCollisonEngine(DummyEngine):
    def derivatives(self, t0, y0):
        self.n=len(self.world)

        y1=Vector(len(y0)) # Pouur stoquer : [vx1, vy1, vx2, vy2, ..., vxn, vyn]

        vect_acc=Vector2(0,0)  # Acceleration

        for i in range(self.n):
            # Vitesse :
            y1[self.dim*i]= y0[(self.n + i)*self.dim]
            y1[self.dim*i+1]= y0[(self.n + i)*self.dim+1]

            pos_i=Vector2(y0[self.dim*i],y0[self.dim*i+1])

            # On l'enregistre pour ne pas avoir a l'appeler a chaque fois
            # mass_i=self.world[i].mass Inutile de multiplier par mass_i pour diviser par mass_i juste après
            if self.world._bodies[i].mass!=0:
                for j in range(i):
                    if self.world._bodies[j].mass!=0:
                        vect_diff=pos_i - Vector2(y0[self.dim*j],y0[self.dim*j+1])
                        d=vect_diff.norm()

                        if d<self.world.seuil_collision:
                            """
                            COLLISION:
                                    Doctrine :  on arrete le calcul,
                                                on fusionne les 2 corps dans 1
                                                l'autre est passé à masse nul
                                                (il sera supprimé plus tard)
                                                on recommence ce calcul
                            """
                            print('      -> COLLISION entre',i,'et',j)

                            # Fusion des données
                            # Recupération des corps à fusionner
                            I=self.world._bodies[i]
                            J=self.world._bodies[j]

                            # Pondération de la vitesse
                            self.world._bodies[i].velocity=(I.mass*I.velocity+J.mass*J.velocity)/(I.mass+J.mass)
                            #self.world._bodies[j].velocity=I.velocity+J.velocity
                            y0[(self.n + i)*self.dim]=self.world._bodies[i].velocity.get_x()
                            y0[(self.n + i)*self.dim+1]=self.world._bodies[i].velocity.get_y()

                            # Ajout des masse
                            self.world._bodies[i].mass+=J.mass
                            # Moyenne des couleurs
                            # self.world._bodies[j].color=((I.color[0]+J.color[0])/2,(I.color[1]+J.color[1])/2,(I.color[2]+J.color[2])/2 )
                            # Max des couleurs
                            self.world._bodies[i].color=(max(I.color[0],J.color[0]),max(I.color[1],J.color[1]),max(I.color[2],J.color[2]))

                            # Rayons
                            self.world._bodies[i].draw_radius=pow(I.draw_radius**2+J.draw_radius**2,0.5)

                            # Mis a 0 de j
                            self.world._bodies[j].mass=0
                            self.world._bodies[j].velocity=Vector2(0,0)
                            self.world._bodies[j].color=self.world.bg_color
                            self.world._bodies[j].draw_radius=0

                            return self.derivatives(t0, y0)

                        else:
                            vect_acc=(-G/(d*d*d))*vect_diff
                            y1[self.dim*self.n + self.dim*i ] += self.world._bodies[j].mass*vect_acc.get_x()
                            y1[self.dim*self.n + self.dim*i+1]+= self.world._bodies[j].mass*vect_acc.get_y()
                            y1[self.dim*self.n + self.dim*j ] += -self.world._bodies[i].mass*vect_acc.get_x()
                            y1[self.dim*self.n + self.dim*j+1]+= -self.world._bodies[i].mass*vect_acc.get_y()

        return y1

