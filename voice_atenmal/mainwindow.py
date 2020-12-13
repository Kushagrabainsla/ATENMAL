import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import QApplication, QDialog
import resource
from out_window import Ui_OutputDialog
import speech_recognition as sr
import multiprocessing
import time

class Ui_Dialog(QDialog):

    def __init__(self):
        super(Ui_Dialog, self).__init__()
        loadUi("main.ui", self)
        self.runButton.clicked.connect(self.runSlot)
        self._new_window = None
        self.Videocapture_ = None


    @pyqtSlot()
    def runSlot(self):
        # Called when the user presses the Run button
        print("Clicked Run")
        self.Videocapture_ = "0"
        self.string_message = ' '
        
        self.speech() # Calling the speech function to hear the status 
        ui.hide()         
        self._new_window = Ui_OutputDialog(self.string_message)
        self._new_window.show()
        self._new_window.startVideo(self.Videocapture_)

    def speech(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Speak 'IN' to checkin and 'OUT' to checkout ")
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio = r.listen(source)
                MyText = r.recognize_google(audio)
                MyText = MyText.lower()
                if MyText == 'in':
                    print("~~~~~You Checked In~~~~~")
                    self.string_message = 'clockin'
                if MyText == 'out':
                    print("~~~~~You Checked Out~~~~~")
                    self.string_message = 'clockout'

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        
        except sr.UnknownValueError:
            print("unknown error occured")              

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())
