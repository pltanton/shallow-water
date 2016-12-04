from . import base
from . import evaluator
import numpy as np

DT = base.GRID_SPACING / 100


class Euler(evaluator.Evaluator):
    def __init__(self, b=0):
        self.b = b

    def evolve(self, h, u, v, g, dt=DT):
        """
        This functionv returns generator, whiche generates euler model steps
        constantly, starts by some given initial state.
        """
        time = 0
        yield h, u, v, time

        while(True):
            delta_dt, du_dt, dv_dt = base.d_dt(h, u, v, g, self.b)

            h += delta_dt * dt
            u += du_dt * dt
            v += dv_dt * dt

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
    h=base.H_0
    u=base.U_0
    v=base.V_0
    g=base.G
    dt=DT
    endTime=0.3
    x,y = np.mgrid[:base.N,:base.N]
    droplet_x, droplet_y = 50, 50
    rr = (x-droplet_x)**2 + (y-droplet_y)**2
    h[rr<10**2] = 3
    # Init generator
    euler = Euler.evolve(h, u, v, g, dt)
    h, u, v, time = next(euler)

    p = gl.GLSurfacePlotItem(z=h, shader='heightColor', color=(0.5, 0.5, 1, 1),
                             smooth=False)
    p.shader()['colorMap'] = np.array([0.2, 2, 0.5, 0.2, 1, 1, 0.2, 0, 2])
    # p.scale(2,2,1)
    p.translate(-base.N/8, -base.N/8, 0)
    p.scale(0.25, 0.25, 1.0)
    w.addItem(p)
    def update():
        global p, euler
        p.setData(z=next(euler)[0])
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(0)
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
