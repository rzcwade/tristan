%%file main.py
#!/usr/bin/env python
import sys
from PyQt4 import QtGui, QtCore, uic
import pyaudio
import numpy as np
import scipy.signal
from scipy.io.wavfile import read as wavread, write as wavwrite
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import wave
import pyaudio
import threading
import atexit
import pyqtgraph as pg
import librosa
from dtw import dtw


try: # static
    from gui import Ui_MainWindow # requires pre-compilation via pyside-uic-* gui.ui > gui.py
except ImportError: # dynamic
    Ui_MainWindow, base = uic.loadUiType("imitationgame.ui")

    
class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        #figure->canvas->widget
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.widget)
        
        
        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.pushButton_2.clicked.connect(self.pushButton_clicked)
        self.pushButton_3.clicked.connect(self.results)
        
    def results(self):
    
        #Loading audio files
        y1, sr1 = librosa.load('output1.wav') 
        y2, sr2 = librosa.load('output2.wav') 
        
        mfcc1 = librosa.feature.mfcc(y1,sr1)   #Computing MFCC values
        mfcc2 = librosa.feature.mfcc(y2, sr2)
            
        dist, cost, path = dtw(mfcc1.T, mfcc2.T)
        
        textEdit_2.appendText(dist)
       
            
    def plot(self):
        ''' plot sound wave '''
      #  fs, x = wavread('output1.wav')
      #  self.graphicsView = pg.ViewBox()
      #  data = pg.PlotDataItem(x)
      #  self.graphicsView.addItem(data)
      #  self.graphicsView.show()
    
        fs, x = wavread('output1.wav')
        
        
        self.figure.set_size_inches(3.5, 1.8)
        #plt.axis('off')
        ax1 = self.figure.add_subplot(2,1,1)
        ax1.axis('off')
        
        #plt.plot(x)
        ax1.plot(x)
        self.canvas.draw()

        
    def plotii(self):
        ''' plot sound wave '''
        
        
        fs, x = wavread('output1.wav')
        
        fs, y = wavread('output2.wav')
        
        self.figure.set_size_inches(3.5, 1.8)
        
            
        ax1 = self.figure.add_subplot(2,1,1)
        ax2 = self.figure.add_subplot(2,1,2)
        
        ax1.axis('off')
        ax2.axis('off')
        
        ax1.plot(x)
        ax2.plot(y)
        self.canvas.draw()
        
        
    def pushButton_clicked(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 5
        
        # Set pushButton clickable in Qt designer
        if self.pushButton.isChecked() == True:
            WAVE_OUTPUT_FILENAME = "output1.wav"
            
        if self.pushButton.isChecked() == True and self.pushButton_2.isChecked() == True:
            WAVE_OUTPUT_FILENAME = "output2.wav"

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        sender = self.sender()
        self.statusBar().showMessage(sender.text() + '* recording')
        #print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

        #print("* done recording")
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + '* done recording')

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()  
        
        #if self.pushButton.isChecked() == True:
          #  self.plot()
            
        if self.pushButton.isChecked() == True and self.pushButton_2.isChecked() == True:
            self.plotii()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

