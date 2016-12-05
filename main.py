import core
import numpy as np

if __name__ == '__main__':
    h = core.base.H_0
    u = core.base.U_0
    v = core.base.V_0
    g = core.base.G
    dt = 0.0001

    typ = 'droplet'
    if typ == 'droplet':
        x, y = np.mgrid[:core.base.N, :core.base.N]
        droplet_x, droplet_y = 50, 50
        rr = (x-droplet_x)**2 + (y-droplet_y)**2
        h[rr < 10**2] = 3
    elif typ == 'wall':
        print('here')
        h[:, :30] = 2

    renderer = core.renderer.Renderer()
    euler = core.euler.Euler(2)
    rk = core.runge_kutta.RungeKutta(2)
    renderer.run(h, u, v, g, dt, rk)
