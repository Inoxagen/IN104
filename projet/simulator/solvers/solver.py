class SolverError(Exception):
    pass


class ISolver:

    # NOTE: our systems do not depend on time,
    # so the input t0 will never be used by the
    # the derivatives function f
    # However, removing it will not simplify
    # our functions so we might as well keep it
    # and build a more general library that
    # we will be able to reuse some day

    def __init__(self, f, t0, y0, max_step_size=0.01):
        self.f = f
        self.t0 = t0
        self.y0 = y0
        self.max_step_size = max_step_size

    def integrate(self, t):
        """ Compute the solution of the system at t
            The input `t` given to this method should be increasing
            throughout the execution of the program.
            Return the new state at time t.
        """

        raise NotImplementedError



class DummySolver(ISolver):
    def integrate(self, t):
        """ Compute the solution of the system at t
            The input `t` given to this method should be increasing
            throughout the execution of the program.
            Return the new state at time t.
        """

        while(self.t0<t):
            y1=self.f(self.t0,self.y0)
            for i in range(len(self.y0)):
                self.y0[i]+=y1[i]
            # pos,vit = pos+vit*1 , vit+acc*1
            self.t0+=1

        return self.y0


"""
class Solver_Euler(ISolver):
    def integrate(self, t):


        while(self.t0<t):
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

            self.t0+=1

        return y0+y1

"""