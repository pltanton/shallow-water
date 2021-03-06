from . import evaluator
from . import base
import numpy as np

DT = base.GRID_SPACING / 100


class RungeKutta(evaluator.Evaluator):
    def __init__(self, b=0, H=np.zeros((100, 100))):
        self.b = b
        self.H = H

    def k_2_3(self, y0, k1, dt):
        h_0, u_0, v_0 = y0
        h_k, u_k, v_k = k1
        dt_2 = dt / 2
        return (h_0 + h_k * dt_2), (u_0 + u_k * dt_2), (v_0 + v_k * dt_2)

    def k_4(self, y0, k3, dt):
        h_0, u_0, v_0 = y0
        h_k, u_k, v_k = k3
        return (h_0 + h_k * dt), (u_0 + u_k * dt), (v_0 + v_k * dt)


    def evolve(self, h, u, v, g, dt=DT):
        time = 0
        yield h, u, v, time

        while True:
            v[-1,:] = np.zeros((100,))
            v[0,:] = -0.9 * v[1,:]
            u[:,-1] = np.zeros((100,))
            u[:,0] = -0.9 * u[:,1]
            y0 = base.d_dt(h, u, v, g, self.b, self.H)
            k1 = y0
            k2 = self.k_2_3(y0, k1, dt)
            k3 = self.k_2_3(y0, k2, dt)
            k4 = self.k_4(y0, k3, dt)

            dh = (dt / 6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            du = (dt / 6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            dv = (dt / 6) * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])

            h += dh
            u += du
            v += dv

            time += dt

            yield h, u, v, time
