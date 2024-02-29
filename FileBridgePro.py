import os
import shutil
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QDialog, QVBoxLayout, QLabel, QLineEdit
from PyQt5 import QtCore

class InputDialog(QDialog):
    def __init__(self, title, label, parent=None):
        super(InputDialog, self).__init__(parent)

        self.setWindowTitle(title)

        self.label = QLabel(label, self)
        self.input_field = QLineEdit(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)

        button_box = self.create_buttons()
        layout.addLayout(button_box)

    def create_buttons(self):
        button_box = QVBoxLayout()

        ok_button = QPushButton('OK', self)
        ok_button.clicked.connect(self.accept)
        button_box.addWidget(ok_button)

        cancel_button = QPushButton('Cancel', self)
        cancel_button.clicked.connect(self.reject)
        button_box.addWidget(cancel_button)

        return button_box

    def get_input(self):
        return self.input_field.text()

class FileTransferApp(QMainWindow):
    def __init__(self):
        super(FileTransferApp, self).__init__()

        self.setWindowTitle("FileBridgePro")
        self.setGeometry(100, 100, 700, 500)

        title_label = QLabel("Transfer your files with Access Control", self)
        title_label.setGeometry(50, 10, 600, 30)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: #173F3F;")

        sender_button = QPushButton("Sender", self)
        sender_button.setGeometry(30, 70, 300, 350)
        sender_button.clicked.connect(self.sender_clicked)
        sender_button.setStyleSheet("background-color: #006400; font-size: 14pt; color: white; border-radius: 10px;")

        receiver_button = QPushButton("Receiver", self)
        receiver_button.setGeometry(370, 70, 300, 350)
        receiver_button.clicked.connect(self.receiver_clicked)
        receiver_button.setStyleSheet("background-color: #173F3F; font-size: 14pt; color: white; border-radius: 10px;")

        copyright_label = QLabel("© 2023 Eagle All Rights Reserved", self)
        copyright_label.setGeometry(50, 470, 600, 20)
        copyright_label.setAlignment(QtCore.Qt.AlignCenter)
        copyright_label.setStyleSheet("font-size: 8pt; color: #000000;")

        # Set a darker background color
        self.setStyleSheet("background-color: #FFFFFF;")

    def sender_clicked(self):
        output = subprocess.check_output('cmd /c "echo %USERNAME%"', shell=True)
        username = output.decode("utf-8").strip()

        userrr = f"{username}"
        destination_folder = f"C:\\Users\\{userrr}\\AppData\\Local\\Temp\\"

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")

        file_name = os.path.basename(file_path)
        file_extension = os.path.splitext(file_name)[1]

        shutil.copy(file_path, destination_folder)

        input_dialog = InputDialog("New File Name", "Enter the new file name", self)
        if input_dialog.exec_():
            new_file_name = input_dialog.get_input()
        else:
            new_file_name = ""
            return  # Added return statement to avoid further execution

        new_file_path = os.path.join(destination_folder, new_file_name + file_extension)

        os.rename(os.path.join(destination_folder, file_name), new_file_path)

        input_dialog = InputDialog("Permission", "Enter the permission (e.g., D,RX)", self)
        if input_dialog.exec_():
            permission = input_dialog.get_input()
        else:
            permission = ""
            return  # Added return statement to avoid further execution

        cmd = f'icacls "{new_file_path}" /grant Everyone:({permission})'
        os.system(cmd)

        print(new_file_path)

        hostname = os.environ['COMPUTERNAME']

        message = f"Hostname: {hostname}\nUsername: {username}\nFile Name: {new_file_name}\nFile Format: {file_extension}"
        QMessageBox.information(self, "Sender Information", message)

    def receiver_clicked(self):
        input_dialog = InputDialog("Input", "Enter the hostname", self)
        if input_dialog.exec_():
            hostname1 = input_dialog.get_input()
        else:
            return

        input_dialog = InputDialog("Input", "Enter the username", self)
        if input_dialog.exec_():
            username1 = input_dialog.get_input()
        else:
            return

        input_dialog = InputDialog("Input", "Enter the file name", self)
        if input_dialog.exec_():
            file_name1 = input_dialog.get_input()
        else:
            return

        input_dialog = InputDialog("Input", "Enter the file extension", self)
        if input_dialog.exec_():
            file_extension1 = input_dialog.get_input()
        else:
            return

        destination_folder = fr'C:\Users\{username1}\AppData\Local\Temp'
        net_path1 = fr'\\{hostname1}{destination_folder.replace("C:", "")}'  

        file_path11 = os.path.join(net_path1, file_name1 + '.' + file_extension1)
        print(file_path11)

        if os.path.exists(file_path11):
            subprocess.run(['start', file_path11], shell=True)
        else:
            print(file_path11)

if __name__ == "__main__":
    app = QApplication([])
    window = FileTransferApp()
    window.show()
    app.exec_()
