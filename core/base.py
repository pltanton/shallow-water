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
    return (np.roll(A, -1, axis) - np.roll(A, 1, axis)) / (GRID_SPACING * 2.)


def d_dx(h):
    return spatial_derivative(h, 1)


def d_dy(h):
    return spatial_derivative(h, 0)


def d_dt(h, u, v, g, b=0):
    """
    Non conservative form from wiki
    """

    du_dt = -g * d_dx(h) - b * u
    dv_dt = -g * d_dy(h) - b * v

    H = 0  # Mean height
    delta_dt = -d_dx(u * (H + h)) - d_dy(v * (H + h))

    return delta_dt, du_dt, dv_dt


def k_1(h, u, v, g, b=0):
    delta_dt, du_dt, dv_dt = d_dt(h, u, v, g, b)
    h = delta_dt
    u = du_dt
    v = dv_dt
    return h, u, v


def k_2(h, u, v, g, b=0):
    k1_h, k1_u, k1_v = k_1(h, u, v, g, b)
    u_2 = -g * d_dx(h + (GRID_SPACING / 2)) - b * (u + (GRID_SPACING * k1_u) / 2)
    v_2 = -g * d_dy(h + (GRID_SPACING / 2)) - b * (v + (GRID_SPACING * k1_v) / 2)

    H = 0  # Mean height
    h_2 = -d_dx((u + (GRID_SPACING * k1_h) / 2) * (H + h + (GRID_SPACING / 2))) - d_dy(
        (v + (GRID_SPACING * k1_v) / 2) * (H + h + (GRID_SPACING / 2)))
    return h_2, u_2, v_2


def k_3(h, u, v, g, b=0):
    k2_h, k2_u, k2_v = k_2(h, u, v, g, b)
    u_3 = -g * d_dx(h + (GRID_SPACING / 2)) - b * (u + (GRID_SPACING * k2_u) / 2)
    v_3 = -g * d_dy(h + (GRID_SPACING / 2)) - b * (v + (GRID_SPACING * k2_v) / 2)

    H = 0  # Mean height
    h_3 = -d_dx((u + (GRID_SPACING * k2_h) / 2) * (H + h + (GRID_SPACING / 2))) - d_dy(
        (v + (GRID_SPACING * k2_v) / 2) * (H + h + (GRID_SPACING / 2)))
    return h_3, u_3, v_3


def k_4(h, u, v, g, b=0):
    k3_h, k3_u, k3_v = k_3(h, u, v, g, b)
    u_4 = -g * d_dx(h + GRID_SPACING) - b * (u + GRID_SPACING * k3_u)
    v_4 = -g * d_dy(h + GRID_SPACING) - b * (v + GRID_SPACING * k3_v)

    H = 0  # Mean height
    h_4 = -d_dx((u + GRID_SPACING * k3_h) * (H + h + GRID_SPACING)) - d_dy(
        (v + GRID_SPACING * k3_v) * (H + h + GRID_SPACING))
    return h_4, u_4, v_4

