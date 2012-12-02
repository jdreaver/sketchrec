from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QTAgg as NavigationToolbar)

from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):

    def __init__(self):
        self.fig = Figure()
        self.fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)
        self.ax = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class matplotlibwidget(QtGui.QWidget):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.canvas.ax.invert_yaxis()
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.vbl.addWidget(self.toolbar)
        self.canvas.ax.set_aspect('equal', 'datalim')

        self.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
            event.button, event.x, event.y, event.xdata, event.ydata)
        if event.button == 2:
            self.toolbar.pan()
        
