# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from main import getResponse


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(970, 716)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        
        # send buttom
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setMaximumSize(QtCore.QSize(80, 45))
        self.sendButton.setStyleSheet("background-color: rgb(0, 170, 127);\n"
"font: 8pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(85, 0, 255);\n"
"font: 75 12pt \"MS Shell Dlg 2\";\n"
"font: 18pt \"MS Shell Dlg 2\";")
        self.sendButton.setObjectName("sendButton")
        self.gridLayout.addWidget(self.sendButton, 1, 1, 1, 1)
        
        # Display button
        self.displayWindow = QtWidgets.QTextEdit(self.centralwidget)
        self.displayWindow.setObjectName("displayWindow")
        self.gridLayout.addWidget(self.displayWindow, 0, 0, 1, 2)
        self.displayWindow.setReadOnly(True)  # Make it read-only
        # Input Window
        self.inputWindow = QtWidgets.QLineEdit(self.centralwidget)
        self.inputWindow.setMinimumSize(QtCore.QSize(300, 0))
        self.inputWindow.setMaximumSize(QtCore.QSize(800, 50))
        self.inputWindow.setPlaceholderText("Ask your question here")
        self.inputWindow.setObjectName("inputWindow")
        self.gridLayout.addWidget(self.inputWindow, 1, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 970, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.sendButton.clicked.connect(self.handle_send_button_click)
    

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sendButton.setText(_translate("MainWindow", "Send"))
    
    def handle_send_button_click(self):
        user_input = self.inputWindow.text()
        if user_input:
            answer = getResponse(user_input)
            self.displayWindow.append(f"<b><font color='blue'>Question:</font></b> {user_input}")
            self.displayWindow.append(f"<b><font face='Tahoma', font color = 'blue'>Answer:</font></b> {answer['generated_text']}")
            self.inputWindow.clear()
        else:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter a question.")


            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
