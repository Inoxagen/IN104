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
        # On recherche le pas fixe de la bonne longueur
        nbr_de_pas= (t-self.t0) // self.max_step_size + 1

        if(nbr_de_pas==0):
             pas_fixe=t-self.t0
        else:
            pas_fixe=(t-self.t0)/nbr_de_pas

        while(self.t0<t):
            y1=self.f(self.t0,self.y0)
            self.y0 += pas_fixe * y1 # pos,vit = pos+vit*pas_fixe , vit+acc*pas_fixe
            self.t0 += pas_fixe
        return self.y0

