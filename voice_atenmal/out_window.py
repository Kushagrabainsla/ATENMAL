from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
from PyQt5.QtWidgets import QDialog
import cv2
import face_recognition
import numpy as np
import datetime
import os
import csv
import yagmail
import serial
import sys
import time 


class Ui_OutputDialog(QDialog):
    def __init__(self, string_message):
        super(Ui_OutputDialog, self).__init__()
        loadUi("./outputwindow.ui", self)

        self.string_message = string_message
        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.Date_Label.setText(current_date)
        self.Time_Label.setText(current_time)
        self.image = None
        self.sendmailbutton.clicked.connect(self.sendmail)
        self.flag = 0
    
    @pyqtSlot()
    def startVideo(self, camera_name):
        if len(camera_name) == 1:
        	self.capture = cv2.VideoCapture(int(camera_name))
        else:
        	self.capture = cv2.VideoCapture(camera_name)
        self.timer = QTimer(self)  # Create Timer
        path = 'ImagesAttendance'
        if not os.path.exists(path):
            os.mkdir(path)
        # known face encoding and known face name list
        images = []
        self.class_names = []
        self.encode_list = []
        self.TimeList1 = []
        self.TimeList2 = []
        attendance_list = os.listdir(path)

        for cl in attendance_list:
            cur_img = cv2.imread(f'{path}/{cl}')
            if cur_img is not None:
                images.append(cur_img)
                self.class_names.append(os.path.splitext(cl)[0])
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(img)
            encodes_cur_frame = face_recognition.face_encodings(img, boxes)[0]
            self.encode_list.append(encodes_cur_frame)
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(10)  # emit the timeout() signal at x=40ms
        
    def sendmail(self):
        print("Mail is working ")
        try:
            yag = yagmail.SMTP('testmail999123484@gmail.com', 'test999123484')
            yag.send(to='testmail999123484@gmail.com', subject='Attendence', contents='Attendence', attachments='Attendance.csv')
            print("Email sent successfully")
        except:
            print("Error, email was not sent")

    def face_rec_(self, frame, encode_list_known, class_names):
    
        def mark_attendance(name, tempe):
            if self.ClockOutButton.isChecked():
                self.ClockOutButton.setEnabled(False)
                with open('Attendance.csv', 'a') as f:
                        if (name != 'unknown'):
                            self.flag = 1
                            date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
                            f.writelines(f'\n{name},{date_time_string},{tempe},Check Out')
                            self.ClockOutButton.setChecked(False)

                            self.NameLabel.setText(name)
                            self.StatusLabel.setText('Checked Out')
                            self.Time2 = datetime.datetime.now()

                            self.ElapseList(name)
                            self.TimeList2.append(datetime.datetime.now())
                            CheckInTime = self.TimeList1[-1]
                            CheckOutTime = self.TimeList2[-1]
                            self.ElapseHours = (CheckOutTime - CheckInTime)
                            self.MinLabel.setText("{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60)%60) + 'm')
                            self.HoursLabel.setText("{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60**2)) + 'h')
                            self.TempLabel.setText(tempe)
                            self.ClockOutButton.setEnabled(True)


            elif self.ClockInButton.isChecked():
                self.ClockInButton.setEnabled(False)
                with open('Attendance.csv', 'a') as f:
                        if (name != 'unknown'):
                            self.flag = 1
                            date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
                            f.writelines(f'\n{name},{date_time_string},{tempe},Check In')
                            self.ClockInButton.setChecked(False)

                            self.NameLabel.setText(name)
                            self.StatusLabel.setText('Checked In')
                            self.HoursLabel.setText('Measuring')
                            self.MinLabel.setText('')
                            self.TempLabel.setText(tempe)
                            self.Time1 = datetime.datetime.now()
                            self.ClockInButton.setEnabled(True)
                            self._new_window.hide()

                            
        # face recognition
        faces_cur_frame = face_recognition.face_locations(frame)
        encodes_cur_frame = face_recognition.face_encodings(frame, faces_cur_frame)
        for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
            match = face_recognition.compare_faces(encode_list_known, encodeFace, tolerance=0.50)
            face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
            name = "unknown"
            best_match_index = np.argmin(face_dis)

            if match[best_match_index]:
                name = class_names[best_match_index].upper()
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 20), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            """
            #This part access temperature for arduino serial monitor.

            arduino_port = "/dev/cu.usbmodem14201" 
            baud = 9600 
            ser = serial.Serial(arduino_port, baud)    
            temp=str(ser.readline())

            #If temperature is normal, click clockin/clockout button.
            
            if temp[2:6] == "None":
                continue
            elif float(temp[2:7]) < 99.1:
                print("Temperature:", temp[2:7],"F")
            tempe = temp[2:7]
            """
            # There are some bugs in the above code, 
            # So until i fix them, i'm using tempe = 99 to show in GUI window.
            # if temp == None:  self.flag = 0 it means then when the previous person will get aside then the flag value wil cange ot  and the next person will get detected.
            if self.string_message == 'clockin':
                self.ClockInButton.setChecked(True)

            if self.string_message == 'clockout':
                self.ClockOutButton.setChecked(True)

            tempe = str(97)
            if self.flag == 0:
                mark_attendance(name, tempe)
        return frame

    def ElapseList(self,name):
        with open('Attendance.csv', "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 2

            Time1 = datetime.datetime.now()
            Time2 = datetime.datetime.now()
            for row in csv_reader:
                for field in row:
                    if field in row:
                        if field == 'Check In':
                            if row[0] == name:
                                #print(f'\t ROW 0 {row[0]}  ROW 1 {row[1]} ROW2 {row[2]}.')
                                Time1 = (datetime.datetime.strptime(row[1], '%y/%m/%d %H:%M:%S'))
                                self.TimeList1.append(Time1)
                        if field == 'Check Out':
                            if row[0] == name:
                                #print(f'\t ROW 0 {row[0]}  ROW 1 {row[1]} ROW2 {row[2]}.')
                                Time2 = (datetime.datetime.strptime(row[1], '%y/%m/%d %H:%M:%S'))
                                self.TimeList2.append(Time2)
                                #print(Time2)

    def update_frame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, self.encode_list, self.class_names, 1)

    def displayImage(self, image, encode_list, class_names, window=1):
        image = cv2.resize(image, (640, 480))
        try:
            image = self.face_rec_(image, encode_list, class_names)
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)
