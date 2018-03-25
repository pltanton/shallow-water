import numpy as np
from . import base
from abc import ABCMeta, abstractmethod

_DT = base.GRID_SPACING / 100

class Evaluator(metaclass=ABCMeta):
    @abstractmethod
    def evolve(self, h, u, v, g, dt=_DT):
        """ Evolves the given system """

    def energy(self, h, u, v, g=base.G):
        keenetic = h * (u ** 2 + v ** 2) / 2
        potential = h ** 2 * g
        full = keenetic + potential
        return np.sum(keenetic), np.sum(potential), np.sum(full)

