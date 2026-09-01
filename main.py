from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import memoryModule
import timingsModule

_translate = QtCore.QCoreApplication.translate

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
        
    def openInfoMenu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_InfoMenu()

        self.ui.setupUi(self.window)
        self.window.show()

    def openTimingsDialog(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = timingsModule.Ui_TimingsDialog()

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
        
        self.infoButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.openInfoMenu())
        self.infoButton.setGeometry(QtCore.QRect(520, 535, 40, 28))
        self.infoButton.setObjectName("infoButton")

        self.timingsButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.openTimingsDialog())
        self.timingsButton.setGeometry(QtCore.QRect(5, 535, 120, 28))
        self.timingsButton.setObjectName("timingsButton")
        self.timingsButton.setText(_translate("MainWindow", "Change Timings"))

        
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
        
        self.infoButton.setText(_translate("MainWindow", "?"))
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

        self.verticalLayout_2.insertWidget(0, self.topicBox)

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
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(50, 141, 150, 30))
        self.label_3.setObjectName("label_3")

        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(20, 50, 141, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Art")
        self.comboBox.addItem("Biology")
        self.comboBox.addItem("Business")
        self.comboBox.addItem("Chemistry")
        self.comboBox.addItem("Computer Science")
        self.comboBox.addItem("DT")
        self.comboBox.addItem("English Literature")
        self.comboBox.addItem("English Language")
        self.comboBox.addItem("French")
        self.comboBox.addItem("Geography")
        self.comboBox.addItem("History")
        self.comboBox.addItem("Mandarin")
        self.comboBox.addItem("Maths")
        self.comboBox.addItem("Ad Maths")
        self.comboBox.addItem("Music")
        self.comboBox.addItem("PE")
        self.comboBox.addItem("Physics")
        self.comboBox.addItem("PSHEE")
        self.comboBox.addItem("Psychology")
        self.comboBox.addItem("RPE")
        self.comboBox.addItem("Sociology")
        self.comboBox.addItem("Spanish")

        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(20, 110, 201, 22))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Dialog)

        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(25, 141, 30, 30))
        self.checkBox.setObjectName("checkBox")

        

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def sendTask(self, button):
        if self.lineEdit.text() == "" and not button.text() == "Cancel":
            self.showWarning()
            return

        if button.text() == "OK":
            if self.checkBox.isChecked() == True and str(2) in timeIntervals:
                task(self.comboBox.currentText(), self.lineEdit.text(), timeIntervals[str(2)], 2)
            else:
                task(self.comboBox.currentText(), self.lineEdit.text(), timeIntervals[str(1)], 1)

        self.Dialog.close()

    def showWarning(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Please enter a topic!")
        msg.setIcon(QMessageBox.Critical)

        msg.exec_()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Active Recall Manager: Create Task"))
        self.label.setText(_translate("Dialog", "Enter Subject"))
        self.label_2.setText(_translate("Dialog", "Enter Topic"))
        self.label_3.setText(_translate("Dialog", "Start on stage 2"))
        self.lineEdit.setText(_translate("Dialog", ""))

class Ui_InfoMenu(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(392, 427)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 40, 311, 61))
        self.label.setAutoFillBackground(False)
        self.label.setScaledContents(False)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 10, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(40, 110, 311, 61))
        self.label_3.setAutoFillBackground(False)
        self.label_3.setScaledContents(False)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(40, 170, 311, 71))
        self.label_4.setAutoFillBackground(False)
        self.label_4.setScaledContents(False)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(40, 250, 311, 81))
        self.label_5.setAutoFillBackground(False)
        self.label_5.setScaledContents(False)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(40, 340, 311, 61))
        self.label_6.setAutoFillBackground(False)
        self.label_6.setScaledContents(False)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")

        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "1. Open your textbook (or your source of information on the subject). Read it through and try and absorb as much information as you can."))
        self.label_2.setText(_translate("Dialog", "How to use Active Recall Manager"))
        self.label_3.setText(_translate("Dialog", "2. Create a new task, filling in all the relevant information. Make sure to not make the topic too vague."))
        self.label_4.setText(_translate("Dialog", "3. When the timer has ran out, grab a piece of paper and write down as much as you can remember from what you learned. You should really rack your brain to find anything - if you find it hard, its working."))
        self.label_5.setText(_translate("Dialog", "4. Once you\'ve finished, grab your source of information, and correct or add on any information you missed out. If you\'re doing this on material you\'ve just learned, you should only expect to remember about a quarter of what you learned."))
        self.label_6.setText(_translate("Dialog", "5. Press Complete, and repeat steps 3-5. Optionally, you could do some practice questions on the topic after you\'ve completed the final stage."))
        QtCore.QMetaObject.connectSlotsByName(Dialog)


timeIntervals = timingsModule.timeIntervals

def iterate():
    global timeIntervals
    timeIntervals = memoryModule.updateTimeIntervals()

    for task in tasks:
        if not task.canBeCompleted:
            task.decreaseTimer()

        if task.stage > timeIntervals.__len__():
            task.UiElements["TopicBox"].deleteLater()
            tasks.remove(task)

        task.UiElements["ProgressBar"].setMaximum(timeIntervals[str(task.stage)])
        task.timeAllowed = timeIntervals[str(task.stage)]

        if task.timePassed > timeIntervals[str(task.stage)]:
            task.timePassed = timeIntervals[str(task.stage)]

class task():
    def __init__(self, subject, topic, time, stage):
        self.subject = subject
        self.topic = topic

        self.timePassed = time

        if time <= 0:
            self.timePassed = 1

        self.stage = stage

        try:
            self.timeAllowed = timeIntervals[str(stage)]
        except:
            return

        if self.timePassed > self.timeAllowed:
            self.timePassed = self.timeAllowed

        self.canBeCompleted = False

        
        tasks.append(self)

        self.UiElements = ui.createTopicBox(self)
        #ui.verticalLayout_2.insertItem(0, self.UiElements["TopicBox"])

    def decreaseTimer(self):
        self.timePassed -= 1

        if self.timePassed > 0:
            self.UiElements["ProgressBar"].setValue(self.timePassed)
            self.UiElements["ProgressLabel"].setText(secondsToDHMS(self.timePassed))
        else:
            self.canBeCompleted = True
            self.UiElements["CompleteButton"].show()
            
            ui.verticalLayout_2.insertWidget(0, self.UiElements["TopicBox"])

    def increaseStage(self):
        
        if self.stage < len(timeIntervals):
            self.stage += 1
            
            self.timeAllowed = timeIntervals[str(self.stage)]
            self.UiElements["ProgressBar"].setRange(0, self.timeAllowed)

            self.timePassed = self.timeAllowed

            self.canBeCompleted = False
            self.UiElements["CompleteButton"].hide()

        else:
            tasks.remove(self)
            self.UiElements["TopicBox"].deleteLater()
        
        self.UiElements["ProgressBar"].value = self.timePassed

    def __str__(self):
        return f"{self.subject}:{self.topic} TimeLeft:{self.timePassed} Stage:{self.stage}"



def quit():
    memoryModule.saveTasks(tasks, timeIntervals)



if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    app.aboutToQuit.connect(quit)

    timer = QtCore.QTimer()

    timer.timeout.connect(iterate)
    timer.start(1000)

    tasksData = memoryModule.tasks
    tasks = []


    for taskItem in tasksData:
        task(taskItem[0], taskItem[1], taskItem[2], taskItem[3])
    
    sys.exit(app.exec_())
