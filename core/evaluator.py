import base
from abc import ABCMeta, abstractmethod

_DT = base.GRID_SPACING / 100

class Evaluator(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def evolve(self, h, u, v, g, dt=_DT):
        """ Evolves the given system """
