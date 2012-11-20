import sys 
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
from mainGUI import Ui_StaticsRecGUI
from sketchrec.imagerec import imageio
#from ..imagerec import imageio
from os.path import isfile

class MainForm(QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__()
        self.ui = Ui_StaticsRecGUI()
        self.ui.setupUi(self)
        
        self.ui.btnLabelTest.clicked.connect(self.TEST_METHOD)

        self.ui.matplot.canvas.mpl_connect('pick_event', self.onpick)
        
        self.selected_strokes = []
        self.setupLabelViews()
        self.ui.btnLabelLoad.clicked.connect(self.load_raw_strokes_test)
        
        self.ui.btnLabel.clicked.connect(self.label_strokes)
        self.ui.labelList.itemSelectionChanged.connect(self.select_label)

    def TEST_METHOD(self):
        print 'LABELS'
        for i, a in enumerate(self.labels):
            print i, a
        print 'GROUPS'
        for group in self.groupings:
            print group

    def load_raw_strokes_test(self):
        self.labelFileName = '/home/david/Dropbox/Research/Data/PencaseDataFix/Pen006/Homework6-Problem1-text.iv'

        templates = imageio.single_stroke_unlabeled_file(self.labelFileName)
        self.stroke_handles = []
        self.labels = []
        self.groupings = []
        for i, t in enumerate(templates):
            x,y = zip(*t.points)
            h, = self.ui.matplot.canvas.ax.plot(x,y, 'k', picker=5)
            h.index = i;
            self.stroke_handles.append(h)
            self.labels.append('NO LABEL')
        self.ui.matplot.canvas.ax.invert_yaxis()
        self.ui.matplot.canvas.draw()
        self.max_xlim = self.ui.matplot.canvas.ax.get_xlim()
        self.max_ylim = self.ui.matplot.canvas.ax.get_ylim()
        self.zoom_fun = zoom_factory(self.ui.matplot.canvas, self.max_xlim,
                                     self.max_ylim, 1.5)

    def onpick(self, event):
        if event.mouseevent.button != 1:
            return 0
        key = QApplication.keyboardModifiers()
        thisline = event.artist
        if key == Qt.ControlModifier:
            self.selected_strokes.append(thisline.index)
        else:
            self.selected_strokes = [thisline.index]
        self.selected_strokes = list(set(self.selected_strokes))
        self.ui.labelText.setText('Selected: ' +
                                  ', '.join(map(str, self.selected_strokes)))

        reset_line_widths(self.stroke_handles)
        for i in self.selected_strokes:
            self.stroke_handles[i].set_linewidth(3)
        self.ui.matplot.canvas.draw()

    def setupLabelViews(self):
        self.ui.labelTree.clear()
        labels = [('Digits','0123456789'), 
                  ('Alphas','AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'),
                  ('Operators', ('plus', 'minus', 'equals', 'divide', 'dot')),
                  ('Misc', ('arrow', 'rparen', 'lparen', 'sigma')),
                  ('NO LABEL', ())]
        for top, sub in labels:
            topWidget = QTreeWidgetItem(self.ui.labelTree)
            topWidget.setText(0, top)
            topWidget.setCheckState(0, Qt.Checked)
            for subLabel in sub:
                labelWidget = QTreeWidgetItem(topWidget)
                labelWidget.setText(0, subLabel)
                labelWidget.setCheckState(0, Qt.Checked)
                listWidget = QListWidgetItem(self.ui.labelList)
                listWidget.setText(subLabel)
        
    def load_raw_strokes(self):
        self.labelFileName = QFileDialog.getOpenFileName()
        print self.labelFileName
        if isfile(self.labelFileName):
            templates = imageio.single_stroke_unlabeled_file(self.labelFileName)
            self.stroke_handles = []
            self.labels = []
            self.groupings = []
            for i, t in enumerate(templates):
                x,y = zip(*t.points)
                h, = self.ui.matplot.canvas.ax.plot(x,y, 'k', picker=5)
                h.index = i;
                self.stroke_handles.append(h)
                self.labels.append('NO LABEL')
            self.ui.matplot.canvas.ax.invert_yaxis()
            self.ui.matplot.canvas.draw()
            self.max_xlim = self.matplot.canvas.ax.get_xlim()
            self.max_ylim = self.matplot.canvas.ax.get_ylim()
            self.zoom_fun = zoom_factory(self.ui.matplot.canvas, self.max_xlim,
                                         self.max_ylim, 1.5)

    def select_label(self):
        selected = self.ui.labelList.selectedItems()[0]
        self.ui.labelLineEdit.setText(selected.text())

    def label_strokes(self):
        label = str(self.ui.labelLineEdit.text()).rstrip()
        if label != '' and self.selected_strokes != []:
            for index in self.selected_strokes:
                self.labels[index] = label
            if self.ui.rdbMultiStroke.isChecked():
                self.groupings.append(self.selected_strokes)
            for i in range(self.ui.labelList.count()):
                if str(self.ui.labelList.item(i).text()) == label:
                    item = self.ui.labelList.takeItem(i)
                    break
            self.ui.labelList.insertItem(0, label)
            self.ui.labelList.setCurrentRow(0)
            self.color_strokes()

    def color_strokes(self):
        handles = self.stroke_handles
        for i, label in enumerate(self.labels):
            if label == 'NO LABEL':
                handles[i].set_color('k')
            else:
                handles[i].set_color('r')
        colors = ['g', 'b', 'c', 'm']
        j = 0
        for group in self.groupings:
            for i in group:
                handles[i].set_color(colors[j % len(colors)])
            j += 1
        self.ui.matplot.canvas.draw()
            

def reset_line_widths(lines):
    for line in lines:
        line.set_linewidth(1)

def zoom_factory(canvas, max_xlim, max_ylim, base_scale = 2.):
    ax = canvas.ax
    def zoom_fun(event):
        # get the current x and y limits
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1/base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
            print event.button
        # set new limits
        #ax.set_xlim([xdata - cur_xrange*scale_factor,
        #             xdata + cur_xrange*scale_factor])
        #ax.set_ylim([ydata - cur_yrange*scale_factor,
        #             ydata + cur_yrange*scale_factor])
        new_xlim = [xdata - cur_xrange*scale_factor,
                    xdata + cur_xrange*scale_factor]
        new_ylim = [ydata - cur_yrange*scale_factor,
                    ydata + cur_yrange*scale_factor]
        ax.set_xlim([max(new_xlim[0], max_xlim[0]),
                     min(new_xlim[1], max_xlim[1])])
        ax.set_ylim([min(new_ylim[0], max_ylim[0]),
                     max(new_ylim[1], max_ylim[1])])
        canvas.draw() # force re-draw

    fig = ax.get_figure() # get the figure of interest
    # attach the call back
    fig.canvas.mpl_connect('scroll_event',zoom_fun)

    #return the function
    return zoom_fun

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainForm()

    window.show()
    #sys.exit(app.exec_())
    app.exec_()
