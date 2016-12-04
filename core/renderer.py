import sys
import numpy as np
from . import base
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl

class Renderer():
    def run(self, h, u, v, g, dt, evaluator, scale=(0.25, 0.25, 1.),
            title='Swallow Water', distance=25):
        ## Create a GL View widget to display data
        app = QtGui.QApplication([])
        w = gl.GLViewWidget()
        w.show()
        w.setWindowTitle(title)
        w.setCameraPosition(distance=distance)

        # Init generator
        gen = evaluator.evolve(h, u, v, g, dt)
        h, u, v, time = next(gen)

        p = gl.GLSurfacePlotItem(z=h, shader='heightColor',
                                 color=(0.5, 0.5, 1, 1),
                                 smooth=False)
        p.shader()['colorMap'] = np.array([0.2, 2, 0.5, 0.2, 1, 1, 0.2, 0, 2])
        p.translate(-base.N/8, -base.N/8, 0)
        p.scale(*scale)
        w.addItem(p)
        def update():
            p.setData(z=next(gen)[0])
        timer = QtCore.QTimer()
        timer.timeout.connect(update)
        timer.start(0)

        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()
