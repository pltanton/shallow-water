import sys
import numpy as np
from . import base
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl

class Renderer():
    def __init__(self, speed=0.001):
        self.speed = speed

    def run(self, h, u, v, g, dt, evaluator, scale=(0.25, 0.25, 1.),
            title='Swallow Water', distance=25):
        ## Create a GL View widget to display data
        app = QtGui.QApplication([])
        w = gl.GLViewWidget()
        w.show()
        w.setWindowTitle(title)
        w.setCameraPosition(distance=distance)

        # Init energy displayer
        text = pg.TextItem('Test', (1,1,1))

        # Init generator
        gen = evaluator.evolve(h, u, v, g, dt)
        h, u, v, time = next(gen)

        # Draw a ground with gred
        ground_array = evaluator.H
        ground = gl.GLSurfacePlotItem(z=ground_array,
                                      color=(0.79, 0.52, 0.22, 1),
                                      smooth=False)
        ground.scale(*scale)
        ground.translate(-base.N/8, -base.N/8,
                         -ground_array.min() - ground_array.max())
        w.addItem(ground)


        p = gl.GLSurfacePlotItem(z=h, shader='balloon',
                                 color=(0.6, 0.5, 1, 0.2),
                                 smooth=False, glOptions='additive')
        # p = gl.GLSurfacePlotItem(z=h, shader='heightColor',
                                 # # color=(0.6, 0.5, 1, 0.2),
                                 # smooth=False)#, glOptions='additive')
        # p.shader()['colorMap'] = np.array([0.2, 0, 1, -0.3, 1, 1, 0.9, 0, 1])
        p.translate(-base.N/8, -base.N/8, 0)
        p.scale(*scale)
        w.addItem(p)
        def update():
            nonlocal time, self
            new_time = time
            h = None
            while new_time - time < self.speed:
                h, u, v, new_time = next(gen)
                print(evaluator.energy(h,u,v)[2])
            time = new_time
            p.setData(z=h)
        timer = QtCore.QTimer()
        timer.timeout.connect(update)
        timer.start(0)

        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()
