""" This module contain basic evaluation required for model """
import numpy as np

N = 100  # Grid size
U_0 = np.zeros((N, N))  # Start velocity in x direction
V_0 = np.zeros((N, N))  # Start velocity in y direction

H_0 = np.zeros((N, N))  # Start values of heights

# Some modeling constants
G = 1.  # Gravity
BOX_SIZE = 1.
GRID_SPACING = 1. * BOX_SIZE / N


def spatial_derivative(A, axis=0):
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
    # if axis == 0:
        # fst[-1,] = A[-1,]
        # snd[0,] = A[0,]
    # elif axis == 1:
        # fst[:,-1] = A[:,-1]
        # snd[:,0] = A[:,0]

    return (fst - snd) / (GRID_SPACING * 2.)


def d_dx(h):
    return spatial_derivative(h, 1)


def d_dy(h):
    return spatial_derivative(h, 0)


def d_dt(h, u, v, g, b=0, H=0):
    """
    Non conservative form from wiki
    """

    du_dt = -g * d_dx(h) - b * u - u * d_dx(u) - v * d_dy(u)
    dv_dt = -g * d_dy(h) - b * v - u * d_dx(v) - v * d_dy(v)

    delta_dt = -d_dx(u * (H + h)) - d_dy(v * (H + h))

    return delta_dt, du_dt, dv_dt
