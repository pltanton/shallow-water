import base
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

DT = base.GRID_SPACING / 100


def evolve(h, u, v, g, dt=DT):
    """
    This functionv returns generator, whiche generates euler model steps
    constantly, starts by some given initial state.
    """
    time = 0
    yield h, u, v, time

    while(True):
        delta_dt, du_dt, dv_dt = base.d_dt(h, u, v, g)

        h += delta_dt * dt
        u += du_dt * dt
        v += dv_dt * dt

        time += dt

        yield h, u, v, time


if __name__ == '__main__':
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
    h[rr<10**2] = 1.1
    # Init generator
    euler = evolve(h, u, v, g, dt)
    # ax = plt.axis(xlim=(0, 100), ylim=(0, 100))
    plt.imshow(h, interpolation='none')
    plt.colorbar()
    plt.ion()
    plt.show()
    time = 0
    h, u, v, time = next(euler)
    step = 0
    while True:
        step += 1
        h, u, v, time = next(euler)
        if step % 100 == 0:
            print('here')
            plt.imshow(h, interpolation='none')
            plt.pause(0.00001)
