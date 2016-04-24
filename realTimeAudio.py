import ui_plot
import sys
import numpy
from PyQt4 import QtCore, QtGui, Qt
import PyQt4.Qwt5 as Qwt
from recorder import *



def increaseY():
    uiplot.qwtPlot.replot()
    yCurrent = uiplot.qwtPlot.axisScaleDiv(uiplot.qwtPlot.yLeft).upperBound()
    uiplot.qwtPlot.setAxisScale(uiplot.qwtPlot.yLeft, 0, yCurrent+5000)

def decreaseY():
    uiplot.qwtPlot.replot()
    yCurrent = uiplot.qwtPlot.axisScaleDiv(uiplot.qwtPlot.yLeft).upperBound()
    uiplot.qwtPlot.setAxisScale(uiplot.qwtPlot.yLeft, 0, yCurrent-5000)


def plotSomething():
    if SR.newAudio==False: 
        return
    xs,ys=SR.fft()
    c.setData(xs,ys)
    uiplot.qwtPlot.replot()
    print SR.energy()
    SR.newAudio=False

if __name__ == "__main__":
    DefaultYaxis = 10000
    app = QtGui.QApplication(sys.argv)
    
    win_plot = ui_plot.QtGui.QMainWindow()
    uiplot = ui_plot.Ui_win_plot()
    uiplot.setupUi(win_plot)
    uiplot.btnA.clicked.connect(lambda: increaseY())
    uiplot.btnB.clicked.connect(lambda: decreaseY())
    #uiplot.btnC.clicked.connect(lambda: uiplot.timer.setInterval(10.0))
    #uiplot.btnD.clicked.connect(lambda: uiplot.timer.setInterval(1.0))

    c=Qwt.QwtPlotCurve()  
    c.attach(uiplot.qwtPlot)
    
    c.setPen(Qt.Qt.blue)

    uiplot.qwtPlot.setAxisTitle(uiplot.qwtPlot.yLeft, "Amplitude/Arb")
    uiplot.qwtPlot.setAxisTitle(uiplot.qwtPlot.xBottom, "Frequency/Hz")
    uiplot.qwtPlot.setAxisScale(uiplot.qwtPlot.yLeft, 0, DefaultYaxis)

   


    uiplot.qwtPlot.setCanvasBackground(Qt.Qt.white)

    uiplot.timer = QtCore.QTimer()
    uiplot.timer.start(1.0)
    
    win_plot.connect(uiplot.timer, QtCore.SIGNAL('timeout()'), plotSomething) 
    
    SR=SwhRecorder()
    SR.setup()
    SR.continuousStart()

    ### DISPLAY WINDOWS
    win_plot.show()
    code=app.exec_()
    SR.close()
    sys.exit(code)
