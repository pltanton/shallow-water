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


if __name__ == '__main__':
    import sys

    ## Create a GL View widget to display data
    app = QtGui.QApplication([])
    w = gl.GLViewWidget()
    w.show()
    w.setWindowTitle('Shallow Water euler')
    w.setCameraPosition(distance=25)

    # TODO: need to refactor, just for test here
    h = base.H_0
    u = base.U_0
    v = base.V_0
    g = base.G
    dt = DT
    endTime = 0.3
    x, y = np.mgrid[:base.N, :base.N]
    droplet_x, droplet_y = 50, 50
    rr = (x - droplet_x) ** 2 + (y - droplet_y) ** 2
    h[rr < 10 ** 2] = 3
    # Init generator
    rungekutta = RungeKutta.evolve(h, u, v, g, dt)
    h, u, v, time = next(rungekutta)

    p = gl.GLSurfacePlotItem(z=h, shader='heightColor', color=(0.5, 0.5, 1, 1),
                             smooth=False)
    p.shader()['colorMap'] = np.array([0.2, 2, 0.5, 0.2, 1, 1, 0.2, 0, 2])
    # p.scale(2,2,1)
    p.translate(-base.N / 8, -base.N / 8, 0)
    p.scale(0.25, 0.25, 1.0)
    w.addItem(p)
