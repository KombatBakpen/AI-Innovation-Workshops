from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap
import os
import sys
import requests

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 981, 721))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.image_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.image_label.setText("")
        self.image_label.setObjectName("image_label")
        self.verticalLayout_3.addWidget(self.image_label)
        self.upload_image_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.upload_image_button.setObjectName("upload_image_button")
        self.verticalLayout_3.addWidget(self.upload_image_button)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.response_textEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.response_textEdit.setMaximumSize(QtCore.QSize(400, 16777215))
        self.response_textEdit.setReadOnly(True)
        self.response_textEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse)
        self.response_textEdit.setObjectName("response_textEdit")
        self.horizontalLayout.addWidget(self.response_textEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.progressBar = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.prompt_lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.prompt_lineEdit.setStyleSheet("background-color: white")  # Changed to white
        self.prompt_lineEdit.setObjectName("prompt_lineEdit")
        self.verticalLayout.addWidget(self.prompt_lineEdit)

        # Set the send button to blue
        self.send_Button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.send_Button.setStyleSheet("background-color: blue; color: white;")
        self.send_Button.setObjectName("send_Button")
        self.verticalLayout.addWidget(self.send_Button)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image to Text UI"))
        self.upload_image_button.setText(_translate("MainWindow", "Upload Image"))
        self.response_textEdit.setPlaceholderText(_translate("MainWindow", ""))
        self.prompt_lineEdit.setPlaceholderText(_translate("MainWindow", "Enter your prompt where..."))
        self.send_Button.setText(_translate("MainWindow", "Send"))

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        
        self.ui.upload_image_button.clicked.connect(self.upload_image)
        self.ui.send_Button.clicked.connect(self.send_prompt_and_image)
        
        self.image_file_path = None

        # ngrok URL 
        self.ngrok_url =  "https://3177-34-145-10-28.ngrok-free.app"  

        
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setVisible(False)

    def upload_image(self):
        # Open file dialog to select an image
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            None, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options
        )

        if file_name:
            if os.path.exists(file_name):
                pixmap = QPixmap(file_name)
                
                if not pixmap.isNull():  
                    scaled_pixmap = pixmap.scaled(
                        self.ui.image_label.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio
                    )
                    self.ui.image_label.setPixmap(scaled_pixmap)
                    self.ui.image_label.setScaledContents(True)
                    self.image_file_path = file_name
                else:
                    self.ui.response_textEdit.setText("Invalid image file. Please select a valid image.")
            else:
                self.ui.response_textEdit.setText("File not found. Please try again.")
        else:
            self.ui.response_textEdit.setText("No file selected.")

    def send_prompt_and_image(self):
        self.ui.response_textEdit.clear() 
        prompt = self.ui.prompt_lineEdit.text().strip()  
        image_path = self.image_file_path


        print(f"Prompt: '{prompt}'")
        print(f"Image Path: '{image_path}'")

        self.ui.response_textEdit.setText("Loading...")
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setValue(50)  

        response_text = None

        try:
            if prompt and image_path:
                print("Both prompt and image provided.")
                api_url = f"{self.ngrok_url}/image"
                with open(image_path, "rb") as image_file:
                    files = {"image": image_file}
                    payload = {"user_input": prompt}
                    response = requests.post(api_url, files=files, data=payload)

                if response.status_code == 200:
                    response_text = response.json().get("response", "No response from the model.")
                else:
                    response_text = f"Error {response.status_code}: {response.text}"

            elif prompt:
                print("Only prompt provided.")
                api_url = f"{self.ngrok_url}/chat"
                payload = {"user_input": prompt}
                response = requests.post(api_url, data=payload)

                if response.status_code == 200:
                    response_text = response.json().get("response", "No response from the model.")
                else:
                    response_text = f"Error {response.status_code}: {response.text}"

            elif image_path:
                response_text = "Only image provided. Please write a prompt."

            else:
                response_text = "You did not provide any prompt or image."

        except requests.exceptions.RequestException as e:
            response_text = f"An error occurred during the API request: {str(e)}"
        except Exception as e:
            response_text = f"An unexpected error occurred: {str(e)}"

        
        if response_text:
            self.ui.response_textEdit.setText(response_text)
        else:
            self.ui.response_textEdit.setText("You did not provide any prompt or image.")

        self.ui.progressBar.setVisible(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
