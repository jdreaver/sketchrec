import sys 
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from mainGUI import Ui_StaticsRecGUI
from sketchrec.imagerec import imageio, grouping
from sketchrec.imagerec.image_template import group_centroid
import os
from os.path import isfile, isdir, basename, dirname, splitext
import os.path

class MainForm(QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__()
        self.ui = Ui_StaticsRecGUI()
        self.ui.setupUi(self)
        
        self.ui.btnLabelTest.clicked.connect(self.TEST_METHOD)

        self.ui.matplot.canvas.mpl_connect('pick_event', self.onpick)
        
        self.selected_strokes = []
        self.stroke_handles = []
        self.setupLabelViews()
        self.ui.btnLabelLoad.clicked.connect(self.load_raw_strokes)
        self.ui.btnLabelSave.clicked.connect(self.save_labels)
        self.ui.btnLabel.clicked.connect(self.label_button)
        self.ui.labelList.itemSelectionChanged.connect(self.select_label)
        self.ui.lblCheckIncremental.stateChanged.connect(self.begin_incremental)

    def TEST_METHOD(self):
        print 'LABELS'
        for i, a in enumerate(self.labels):
            print i, a
        print 'GROUPS'
        for group in self.groupings:
            print group

    def begin_incremental(self, event):
        if self.stroke_handles and \
               self.ui.lblCheckIncremental.checkState() == Qt.Checked:
                # Find first unlabeled stroke:
                for j, label in enumerate(self.labels):
                    if label == "NO LABEL":
                        self.selected_strokes = [j]
                        break
                self.update_selected_strokes()

    def keyPressEvent(self, event):
        if self.ui.lblCheckIncremental.checkState() == Qt.Checked and \
           self.stroke_handles:
            key = event.key()
            key_string = str(event.text())
            print key, key_string
            if key == Qt.Key_Space and self.selected_strokes[0] < self.num_temps:
                self.selected_strokes = [self.selected_strokes[0] + 1]
            elif key == Qt.Key_Backspace and self.selected_strokes[0] > 0:
                self.selected_strokes = [self.selected_strokes[0] - 1]
            elif key == Qt.Key_Right and self.selected_strokes[-1] < self.num_temps:
                self.selected_strokes.append(self.selected_strokes[-1] + 1)
            elif key == Qt.Key_Left and len(self.selected_strokes) > 1:
                self.selected_strokes.pop()
            elif key_string in key_to_label.keys():
                bool_grouped = True if len(self.selected_strokes) > 1 else False
                self.label_strokes(key_to_label[key_string], bool_grouped)
                self.selected_strokes = [self.selected_strokes[-1] + 1]
            self.update_selected_strokes()
            if self.ui.lblCheckIncFollow.isChecked() and self.selected_strokes:
                self.recenter_axes_on_selected()

    def recenter_axes_on_selected(self):
        ax = self.ui.matplot.canvas.ax
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        templates = [self.templates[i] for i in self.selected_strokes]
        centroid = group_centroid(templates)
        xdata = centroid[0]
        ydata = centroid[1]
        # set new limits
        new_xlim = [xdata - cur_xrange,
                    xdata + cur_xrange]
        new_ylim = [ydata - cur_yrange,
                    ydata + cur_yrange]
        ax.set_xlim(new_xlim)
        ax.set_ylim(new_ylim)
        self.ui.matplot.canvas.draw() # force re-draw
        

    def load_raw_strokes(self):
        #self.labelFileName = '/home/david/Dropbox/Research/Data/PencaseDataFix/Pen006/Homework6-Problem1-text.iv'
        self.labelFileName = str(QFileDialog.getOpenFileName())
        if isfile(self.labelFileName):
            self.pen = basename(dirname(self.labelFileName))
            self.file_name = splitext(basename(self.labelFileName))[0]
            self.templates = imageio.single_stroke_unlabeled_file(self.labelFileName)
            self.num_temps = len(self.templates)
            self.stroke_handles = []
            self.labels = []
            self.groupings = []
            self.ui.matplot.canvas.ax.clear()
            for i, t in enumerate(self.templates):
                x,y = zip(*t.points)
                h, = self.ui.matplot.canvas.ax.plot(x,y, 'k', picker=5)
                h.index = i;
                self.stroke_handles.append(h)
                self.labels.append('NO LABEL')
            self.ui.matplot.canvas.draw()
            self.max_xlim = self.ui.matplot.canvas.ax.get_xlim()
            self.max_ylim = self.ui.matplot.canvas.ax.get_ylim()
            self.zoom_fun = zoom_factory(self.ui.matplot.canvas, self.max_xlim,
                                         self.max_ylim, 1.5)

    def save_labels(self):
        dir_name = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if isdir(dir_name):
            base_dir = os.path.join(dir_name, self.pen)
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)
            out_base = os.path.join(base_dir, self.file_name)
            
            label_out = str(len(self.labels)) + '\n' + '\n'.join(self.labels)
            label_file = out_base + '.lbl'
            groups = grouping.sparse_groups_to_groups(self.groupings,
                                                          self.num_temps)
            groups_out = str(len(groups)) + '\n' + \
                         '\n'.join([' '.join(map(str, g)) for g in groups])
            groups_file = out_base + '.grp'

            open(label_file, 'w').write(label_out)
            open(groups_file, 'w').write(groups_out)
            
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
        self.selected_strokes = sorted(self.selected_strokes)
        
        self.update_selected_strokes()

    def update_selected_strokes(self):
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
                  ('Operators', ('plus', 'minus', 'equal', 'divide', 'dot')),
                  ('Misc', ('arrow', 'rparen', 'lparen', 'sigma', 'circle', 'decimal',
                            'box', 'squigglebox', 'ampersand')),
                  ('NO LABEL', ())]
        for top, sub in labels:
            topWidget = QTreeWidgetItem(self.ui.labelTree)
            topWidget.setText(0, top)
            topWidget.setCheckState(0, Qt.Checked)
            for subLabel in sub:
                if subLabel.islower() and len(subLabel) == 1:
                    subLabel += subLabel
                labelWidget = QTreeWidgetItem(topWidget)
                labelWidget.setText(0, subLabel)
                labelWidget.setCheckState(0, Qt.Checked)
                listWidget = QListWidgetItem(self.ui.labelList)
                listWidget.setText(subLabel)
        self.ui.labelTree.itemChanged.connect(self.label_tree_item_changed)
                
    def label_tree_item_changed(self, widget_item, column):
        checked = widget_item.checkState(0)
        [widget_item.child(i).setCheckState(0, checked) for i
         in range(widget_item.childCount())]
            
        
    def select_label(self):
        selected = self.ui.labelList.selectedItems()[0]
        self.ui.labelLineEdit.setText(selected.text())

    def label_button(self):
        label = str(self.ui.labelLineEdit.text()).rstrip()
        if label != '' and self.selected_strokes != []:
            bool_grouped = True if self.ui.rdbMultiStroke.isChecked() else False
            self.label_strokes(label, bool_grouped)

    def label_strokes(self, label, bool_grouped):
        self.remove_from_groups(self.selected_strokes)
        if bool_grouped and len(self.selected_strokes) > 1:
            self.groupings.append(self.selected_strokes)
        for index in self.selected_strokes:
            self.labels[index] = label
        for i in range(self.ui.labelList.count()):
            if str(self.ui.labelList.item(i).text()) == label:
                item = self.ui.labelList.takeItem(i)
                break
        self.ui.labelList.insertItem(0, label)
        self.ui.labelList.setCurrentRow(0)
        self.color_strokes()

    def remove_from_groups(self, new_group):
        for index in new_group:
            for group in self.groupings:
                if index in group:
                    for g in group:
                        self.labels[g] = "NO LABEL"
                    self.groupings.remove(group)
        
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

key_to_label = {'+':'plus',
                '-':'minus',
                '=':'equals',
                '(':'lparen',
                ')':'rparen',
                '.':'decimal',
                '<':'arrow',
                '>':'arrow',
                '@':'circle',
                '*':'dot',
                '!':'sigma',
                '&':'ampersand',
                '[':'box',
                '{':'squigglebox'}

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    key_to_label[letter] = letter
    key_to_label[letter.lower()] = 2*letter.lower()
for num in '01234567890':
    key_to_label[num] = num


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainForm()

    window.show()
    #sys.exit(app.exec_())
    app.exec_()
