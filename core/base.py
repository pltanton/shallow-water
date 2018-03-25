""" This module contain basic evaluation required for model """
import numpy as np

N = 100  # Grid size
U_0 = np.zeros((N, N))  # Start velocity in x direction
V_0 = np.zeros((N, N))  # Start velocity in y direction

H_0 = np.ones((N, N))  # Start values of heights

# Some modeling constants
G = 1.  # Gravity
BOX_SIZE = 1.
GRID_SPACING = 1. * BOX_SIZE / N


def spatial_derivative(A, axis=0, fix_bound=False):
    """
    Compute derivative of array A using balanced finite differences
    Axis specifies direction of spatial derivative (d/dx or d/dy)
    dA[i] =  A[i+1] - A[i-1]   / 2
    ... or with grid spacing included ...
    dA[i]/dx =  A[i+1] - A[i-1]   / 2dx
    Used By:
        d_dx
        d_dy
    """
    fst = np.roll(A, -1, axis)
    snd = np.roll(A, 1, axis)
    result = (fst - snd) / (GRID_SPACING * 2.)
    if fix_bound:
        result[0,:] = result[-1,:] = result[:,0] = result[:,-1] = np.zeros((100,))
    return result


def d_dx(h, fix_bound=False):
    return spatial_derivative(h, 1, fix_bound)


def d_dy(h, fix_bound=False):
    return spatial_derivative(h, 0, fix_bound)


def d_dt(h, u, v, g, b=0, H=0):
    """
    Non conservative form from wiki
    """

    # print((- u * d_dx(u) - v * d_dy(u))[50, 10])
    du_dt = -g * d_dx(h) - b * u #- u * d_dx(u, True) - v * d_dy(u, True)
    dv_dt = -g * d_dy(h) - b * v #- u * d_dx(v, True) - v * d_dy(v, True)

    delta_dt = -d_dx(u * (H + h)) - d_dy(v * (H + h))

    return delta_dt, du_dt, dv_dt
