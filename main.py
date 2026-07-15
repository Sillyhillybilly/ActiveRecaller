from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import time
import json
_translate = QtCore.QCoreApplication.translate

timeIntervals = {
    1 : 600,
    2 : 10800,
    3 : 86400,
    4 : 172800,
    5 : 604800
}

     
tasks = []

def secondsToDHMS(seconds):
    days, modDays = seconds // 86400, seconds % 86400
    hours, modHours = modDays // 3600, modDays % 3600
    minutes, seconds = modHours // 60, modHours % 60

    return f"{days:02} : {hours:02} : {minutes:02} : {seconds:02}"

#-------------MAIN WINDOW---------------#
class Ui_MainWindow(object):
    def openTopicDialog(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Dialog()

        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(570, 588)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(50, 130, 471, 381))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 448, 379))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")


        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.openTopicDialog())
        self.pushButton.setGeometry(QtCore.QRect(50, 80, 451, 28))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 680, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Active Recall Manager"))
        
        self.pushButton.setText(_translate("MainWindow", "Create new topic"))

    def createTopicBox(self, task):

        self.topicBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topicBox.sizePolicy().hasHeightForWidth())
        self.topicBox.setSizePolicy(sizePolicy)
        self.topicBox.setMinimumSize(QtCore.QSize(412, 60))
        self.topicBox.setObjectName("topicBox")


        self.topicLabel = QtWidgets.QLabel(self.topicBox)
        self.topicLabel.setGeometry(QtCore.QRect(20, 20, 102, 31))
        self.topicLabel.setObjectName("topicLabel")

        timeAllowed = task.timeAllowed
        timePassed = task.timePassed


        self.progressLabel = QtWidgets.QLabel(self.topicBox)
        self.progressLabel.setGeometry(QtCore.QRect(150, 10, 161, 16))
        self.progressLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.progressLabel.setObjectName("progressLabel")

        self.completeButton = QtWidgets.QPushButton(self.topicBox, clicked = lambda : self.increaseStage(task))
        self.completeButton.setGeometry(QtCore.QRect(331, 20, 71, 32))
        self.completeButton.setObjectName("completeButton")

        self.completeButton.hide()

        self.verticalLayout_2.addWidget(self.topicBox)

        #PROGRESS BAR
        self.progressBar = QtWidgets.QProgressBar(self.topicBox)
        self.progressBar.setGeometry(QtCore.QRect(140, 30, 181, 23))
        
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(timeAllowed)

        self.progressBar.setValue(timePassed)

        self.progressBar.setTextVisible(False)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")

        
        self.topicBox.setTitle(_translate("MainWindow", task.subject))
        self.topicLabel.setText(_translate("MainWindow", task.topic))
        self.progressLabel.setText(_translate("MainWindow", secondsToDHMS(timePassed)))
        self.completeButton.setText(_translate("MainWindow", "Ready!"))

        return {
            "TopicBox" : self.topicBox,
            "TopicLabel" : self.topicLabel,
            "ProgressBar" : self.progressBar,
            "ProgressLabel" : self.progressLabel,
            "CompleteButton" : self.completeButton
        }

    def increaseStage(self, task):
        if not task.canBeCompleted:
            return

        task.increaseStage()

# -------DIALOG---------#
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        
        self.Dialog = Dialog

        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 292)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)

        self.buttonBox.clicked.connect(self.sendTask)

        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 30, 151, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 151, 16))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(20, 50, 141, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(20, 110, 201, 22))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def sendTask(self, button):
        if self.lineEdit.text() == "" and not button.text() == "Cancel":
            self.showWarning()
            return

        if button.text() == "OK":
            task(self.comboBox.currentText(), self.lineEdit.text(), timeIntervals[1], 1)

        self.Dialog.close()

    def showWarning(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Please enter a topic!")
        msg.setIcon(QMessageBox.Critical)

        msg.exec_()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Enter Subject"))
        self.label_2.setText(_translate("Dialog", "Enter Topic"))
        self.comboBox.setItemText(0, _translate("Dialog", "English Lit."))
        self.comboBox.setItemText(1, _translate("Dialog", "English Lang."))
        self.comboBox.setItemText(2, _translate("Dialog", "Physics"))
        self.comboBox.setItemText(3, _translate("Dialog", "DT"))
        self.comboBox.setItemText(4, _translate("Dialog", "RPE"))
        self.comboBox.setItemText(5, _translate("Dialog", "Chemistry"))
        self.comboBox.setItemText(6, _translate("Dialog", "Ad Maths"))
        self.comboBox.setItemText(7, _translate("Dialog", "Biology"))
        self.comboBox.setItemText(8, _translate("Dialog", "Computing"))
        self.comboBox.setItemText(9, _translate("Dialog", "Maths"))
        self.comboBox.setItemText(10, _translate("Dialog", "French"))
        self.lineEdit.setText(_translate("Dialog", ""))


def execute():
    for task in tasks:
        if not task.canBeCompleted:
            task.decreaseTimer()

class task():
    def __init__(self, subject, topic, time, stage):
        self.subject = subject
        self.topic = topic

        self.timePassed = time

        if time <= 0:
            self.timePassed = 1

        self.stage = stage
        self.timeAllowed = timeIntervals[stage]

        if self.timePassed > self.timeAllowed:
            self.timePassed = self.timeAllowed

        self.canBeCompleted = False

        
        tasks.append(self)

        self.UiElements = ui.createTopicBox(self)

    def decreaseTimer(self):
        self.timePassed -= 1

        if self.timePassed != 0:
            self.UiElements["ProgressBar"].setValue(self.timePassed)
            self.UiElements["ProgressLabel"].setText(secondsToDHMS(self.timePassed))
        else:
            self.canBeCompleted = True
            self.UiElements["CompleteButton"].show()

    def increaseStage(self):
        
        if self.stage < len(timeIntervals):
            self.stage += 1
            
            self.timeAllowed = timeIntervals[self.stage]
            self.UiElements["ProgressBar"].setRange(0, self.timeAllowed)

            self.timePassed = self.timeAllowed

            self.canBeCompleted = False
            self.UiElements["CompleteButton"].hide()
        else:
            tasks.remove(self)
            self.UiElements["TopicBox"].deleteLater()
        
        self.UiElements["ProgressBar"].value = self.timePassed

#READ DATA

def readTasks():
    try:
        with open("tasks", "r") as f:
            data = json.load(f)
            timeLoaded = data["TimeLoaded"]
            
            timeNow = int(time.time())
            timeSinceLastInstance = timeNow - timeLoaded
            tasks = []
            for item in data["Tasks"]:
                t = item["Time"] - timeSinceLastInstance
                taskEntry = task(item["Subject"], item["Topic"], t, item["Stage"])

                tasks.append(taskEntry)

    except FileNotFoundError:
            tasks = []
#SAVE DATA
def saveTasks():
    with open("tasks", "w") as f:

        data = {
            "TimeLoaded" : int(time.time()),
            "Tasks" : []
        }

        for task in tasks:
            taskData = {
                "Subject" : task.subject,
                "Topic" : task.topic,
                "Time" : task.timePassed,
                "Stage" : task.stage
            }

            data["Tasks"].append(taskData)

        json.dump(data, f)





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)

    MainWindow.show()

    readTasks()
    app.aboutToQuit.connect(saveTasks)

    timer = QtCore.QTimer()

    timer.timeout.connect(execute)
    timer.start(1000)

    sys.exit(app.exec_())


