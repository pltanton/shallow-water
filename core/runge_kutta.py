from . import evaluator
from . import base
import numpy as np

DT = base.GRID_SPACING / 100


class RungeKutta(evaluator.Evaluator):
    def __init__(self, b=0):
        self.b = b

    def evolve(self, h, u, v, g, dt=DT):
        time = 0
        yield h, u, v, time

        while True:
            k1_h, k1_u, k1_v = base.k_1(h, u, v, g, self.b)
            k2_h, k2_u, k2_v = base.k_2(h, u, v, g, self.b)
            k3_h, k3_u, k3_v = base.k_3(h, u, v, g, self.b)
            k4_h, k4_u, k4_v = base.k_4(h, u, v, g, self.b)

            dh = (dt / 6) * (k1_h + 2 * k2_h + 2 * k3_h + k4_h)
            du = (dt / 6) * (k1_u + 2 * k2_u + 2 * k3_u + k4_u)
            dv = (dt / 6) * (k1_v + 2 * k2_v + 2 * k3_v + k4_v)

            h += dh
            u += du
            v += dv

            time += dt

            yield h, u, v, time
