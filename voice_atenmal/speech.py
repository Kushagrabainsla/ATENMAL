"""
import speech_recognition as sr
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

r = sr.Recognizer()


class input_voice():
    def __init__(self):
        loadUi("./outputwindow.ui", self)
        self.ClockOutButton.setChecked(False)
        self.ClockInButton.setChecked(False)
        self.function()


    def function(self):

        while True:
            try:
                with sr.Microphone() as source:
                    print("Speak 'check in' to checkin and 'check out' to checkout ")
                    r.adjust_for_ambient_noise(source, duration=0.2)
                    audio = r.listen(source)
                    MyText = r.recognize_google(audio)
                    MyText = MyText.lower()
                    if MyText == 'check in':
                        self.ClockInButton.setChecked(True)
                        print("~~~~~You Checked In~~~~~")
                    if MyText == 'check out':
                        self.ClockOutButton.setChecked(True)
                        print("~~~~~You Checked Out~~~~~")
                    if MyText == 'thank you':
                        print("~~~~~Your Welcome~~~~~")
                        break
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
        
            except sr.UnknownValueError:
                print("unknown error occured")
"""
"""
haha = input_voice()
haha.function
"""

import speech_recognition as sr
import multiprocessing
import time

def speech(string_message):
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
                string_message = 'clockin'
            if MyText == 'out':
                print("~~~~~You Checked Out~~~~~")
                string_message = 'clockout'

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        
    except sr.UnknownValueError:
        print("unknown error occured")

print("haha")
string_message = ' '
p = multiprocessing.Process(target= speech, name="Function", args=(string_message, ))
p.start()
time.sleep(10)
p.terminate()
p.join()
print(string_message)

