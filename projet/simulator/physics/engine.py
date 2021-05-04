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


         # [vx1, vy1, vx2, vy2, ..., vxn, vyn]
        y1=Vector(2*self.dim*self.n)

        for i in range(self.n):
            # Vitesse
            y1[self.dim*i]= y0[(self.n + i)*self.dim]
            y1[self.dim*i+1]= y0[(self.n + i)*self.dim+1]

            # Acceleration
            acc_i=Vector2(0,0)
            pos_i=Vector2(y0[self.dim*i],y0[self.dim*i+1]) # On l'enregistre pour ne pas avoir a l'appeler a chaque fois
            # mass_i=self.world[i].mass Inutile de multiplier par mass_i pour diviser par mass_i juste après

            for j in range(self.n):
                if(i!=j):
                    acc_i+=gravitational_force(pos_i, 1, Vector2(y0[self.dim*j],y0[self.dim*j+1]), self.world._bodies[j].mass)

            y1[self.dim*self.n + self.dim*i ] = acc_i.get_x()
            y1[self.dim*self.n + self.dim*i+1]= acc_i.get_y()

        return y1


    def make_solver_state(self):
        """ Returns the state given to the solver, it is the vector y in
                y' = f(t, y)
            In our case, it is the vector containing the
            positions and speeds of all our bodies:
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.
        """

        y=Vector(4*self.n)

        for i in range(self.n):
            y[self.dim*i]= self.world._bodies[i].position.get_x()
            y[self.dim*i+1]= self.world._bodies[i].position.get_y()
            y[self.dim*self.n + self.dim*i ] = self.world._bodies[i].velocity.get_x()
            y[self.dim*self.n + self.dim*i+1]= self.world._bodies[i].velocity.get_y()
        return y


"""
class Engine_Euler:
    def make_solver_state(self):
        #n_accelerations=[] # Contient tte les N accerations donné par le PFD respectivement de nos N objets
        y0=[]
        y1=[]
        for i in range(self.n):
            acc_i=0
            pos_i=self.world._bodies[i].position # On l'enregistre pour ne pas avoir a l'appeler a chaque fois
            # mass_i=self.world[i].mass Inutile de multiplier par mass_i pour diviser par mass_i juste après
            for j in range(self.n):
                if(i!=j):
                    acc_i+=gravitational_force(pos_i, 1,self.world._bodies[j].position, self.world._bodies[j].mass)
            #n_accelerations.append(acc_i)

            # On modifie directement les vitesses
            self.world._bodies[i].velocity+=acc_i
            y1.append(self.world._bodies[i].velocity)


        for i in range(self.n):
        # Integration des positions
            self.world._bodies[i].position+=self.world._bodies[i].velocity
            y0.append(self.world._bodies[i].position)

        self.world.t0+=1

        return y0+y1
"""
