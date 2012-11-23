import numpy as np
import matplotlib.pyplot as plt
''' see http://matplotlib.sourceforge.net/users/event_handling.html for more examples.'''

class LinePicker:
    def __init__(self,xs,ys):

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title('click on a line to make it thick')

        self.handles = []
        for x,y in zip(xs,ys):
            #note use of the comma after the handle
            h, = ax.plot(x,y, '-', picker=5)
            self.handles.append(h)

        fig.canvas.mpl_connect('pick_event', self.onpick)

        self.lastartist = self.handles[-1]

        plt.show()

    def onpick(self,event):
        self.lastartist.set_linewidth(1)
        self.lastartist = thisline = event.artist
        thisline.set_linewidth(6)

        plt.draw()


x = np.linspace(0,np.pi,100)
y1 = np.cos(x)
y2 = np.sin(x)


LinePicker(xs=[x,x],ys=[y1,y2])
