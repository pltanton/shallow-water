import core
import numpy as np

if __name__ == '__main__':
    h = core.base.H_0
    u = core.base.U_0
    v = core.base.V_0
    g = core.base.G
    dt = 0.00004

    # Initial state of water
    typ = 'wall'
    if typ == 'droplet':
        x, y = np.mgrid[:core.base.N, :core.base.N]
        droplet_x, droplet_y = 50, 50
        rr = (x-droplet_x)**2 + (y-droplet_y)**2
        h[rr < 3**2] = 3
    elif typ == 'wall':
        h[:, 1] = 8

    # Initiate ground
    ctg_bound = 2
    ctg_base = np.array([np.tanh(i) for i in np.arange(-ctg_bound+1,
                                                       ctg_bound+1,
                                                       ctg_bound/50)])
    ground_base = ctg_base * 5 + 4
    ground = ground_base.repeat(100).reshape((100, 100)).transpose()

    renderer = core.renderer.Renderer(speed=0.001)
    euler = core.euler.Euler(1, ground)
    max_point = 10
    min_point = 0
    step = (max_point - min_point) / 100
    H = np.array([np.arange(min_point, max_point, step) for _ in range(100)])
    rk = core.runge_kutta.RungeKutta(3, ground)
    renderer.run(h, u, v, g, dt, rk)
