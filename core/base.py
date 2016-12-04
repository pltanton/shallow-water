""" This module contain basic evaluation required for model """
import numpy as np

N = 100  # Grid size
U_0 = np.zeros((N, N))  # Start velocity in x direction
V_0 = np.zeros((N, N))  # Start velocity in y direction

H_0 = np.ones((N, N))  # Start values of heights

# Some modeling contstants
G = 1.  # Gravity
BOX_SIZE = 1.
GRID_SPACING = 1.*BOX_SIZE / N


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
    return (np.roll(A, -1, axis) - np.roll(A, 1, axis)) / (GRID_SPACING*2.)


def d_dx(h):
    return spatial_derivative(h, 1)


def d_dy(h):
    return spatial_derivative(h, 0)



def d_dt(h, u, v, g, b=0):
    """
    Non conservative form from wiki
    """

    du_dt = -g*d_dx(h) - b*u
    dv_dt = -g*d_dy(h) - b*v

    H = 0  # Mean height
    delta_dt = -d_dx(u * (H+h)) - d_dy(v * (H+h))

    return delta_dt, du_dt, dv_dt

