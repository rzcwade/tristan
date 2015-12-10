#!/usr/bin/env python
import sys
from PyQt4 import QtGui, uic
import pyaudio
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import wave
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
        
        #initialize a rank array to hold all the scores
        self.rank = []
        self.count = 0
        #string holder for displaying score
        self.outputRank = ""
        
        #figure->canvas->widget
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.widget)
        
        #events
        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.pushButton_2.clicked.connect(self.pushButton_clicked)
        self.pushButton_3.clicked.connect(self.results)
        self.pushButton_4.clicked.connect(self.ranks)
        
    def results(self):
    
        #Loading audio files
        #Extract MFCC features and use dtw to compare the distance between two MFCCs
        y1, sr1 = librosa.load('output1.wav') 
        y2, sr2 = librosa.load('output2.wav') 
        
        mfcc1 = librosa.feature.mfcc(y1,sr1)   #Computing MFCC values
        mfcc2 = librosa.feature.mfcc(y2,sr2)
            
        dist, cost, path = dtw(mfcc1.T, mfcc2.T)
        
        #Set a threshold for our game's ranking system
        if dist <= 40:
            self.textEdit_2.setText("You did a great job! ^^")
        elif dist <= 50:
            self.textEdit_2.setText("You did good.")
        elif dist <= 60:
            self.textEdit_2.setText("You're fine.")
        else:
            self.textEdit_2.setText("You are poor at this game... TT")
            
        
        self.rank.append(dist)
        self.textEdit_3.setText(str(self.rank[self.count]))
        self.outputRank += "Player " + str(self.count) + " got " + str(self.rank[self.count]) + "\n\n"      
        self.count = self.count + 1
        
        
            
    def ranks(self):
           
        self.textEdit_3.setText(self.outputRank)
        
            
    def plot(self):
        ''' plot sound wave '''
    
#        fs, x = wavread('output1.wav')
        y1, sr1 = librosa.load('output1.wav') 
        y2, sr2 = librosa.load('output2.wav') 
        
        self.figure.set_size_inches(4.5, 2.0)
        #plt.axis('off')
        ax1 = self.figure.add_subplot(2,1,1)
        ax1.axis('off')
        
        ax1.plot(y1)
        self.canvas.draw()

        
    def plotii(self):
        ''' plot sound wave '''
        #clear the previous canvas that holds the first plot
        #the reason that I did this is because I couldn't figure out how to use two canvases 
        #at the same time in one application
        self.figure.clf()        
        
        y1, sr1 = librosa.load('output1.wav') 
        y2, sr2 = librosa.load('output2.wav') 
        
        self.figure.set_size_inches(4.5, 2.0)
        
            
        ax1 = self.figure.add_subplot(2,1,1)
        ax2 = self.figure.add_subplot(2,1,2)
        
        ax1.axis('off')
        ax2.axis('off')
        
        ax1.plot(y1)
        ax2.plot(y2)
        self.canvas.draw()
        
        self.pushButton_2.setChecked(False) 
        
        
    def pushButton_clicked(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 1
        
        # Set pushButton clickable in Qt designer
        if self.pushButton.isChecked() == True:
            WAVE_OUTPUT_FILENAME = "output1.wav"
            
        if self.pushButton.isChecked() == True and self.pushButton_2.isChecked() == True:
            WAVE_OUTPUT_FILENAME = "output2.wav"
            
        #Courtesy of https://people.csail.mit.edu/hubert/pyaudio/#examples
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
        
        #choose plotting methods when different buttons are pushed
        if self.pushButton.isChecked() == True:
            self.plot()
            
        if self.pushButton.isChecked() == True and self.pushButton_2.isChecked() == True:
            self.plotii()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
