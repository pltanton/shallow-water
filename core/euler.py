from . import base
from . import evaluator
import numpy as np

DT = base.GRID_SPACING / 100


class Euler(evaluator.Evaluator):
    def __init__(self, b=0):
        self.b = b

    def evolve(self, h, u, v, g, dt=DT):
        """
        This function v returns generator, which generates euler model steps
        constantly, starts by some given initial state.
        """
        time = 0
        yield h, u, v, time

        while True:
            delta_dt, du_dt, dv_dt = base.d_dt(h, u, v, g, self.b)
            h += delta_dt * dt
            u += du_dt * dt
            v += dv_dt * dt

            time += dt

            yield h, u, v, time
