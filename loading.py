from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox
from request import *
from database import Database
from out_table import Ui_Form
from PyQt6.QtCore import QRunnable, QObject, QThreadPool, QThread, pyqtSignal, pyqtSlot as Slot
import threading


    

class Ui_Window(object):
    def setupUi(self, Window):
        Window.setObjectName("Window")
        Window.resize(391, 187)
        Window.setMinimumSize(QtCore.QSize(391, 187))
        Window.setMaximumSize(QtCore.QSize(391, 187))
        Window.setWindowIcon(QIcon('logo.png'))
        self.verticalLayout = QtWidgets.QVBoxLayout(Window)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Window)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.page_1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.first_page_label = QtWidgets.QLabel(self.page_1)
        self.first_page_label.setMinimumSize(QtCore.QSize(0, 120))
        self.first_page_label.setMaximumSize(QtCore.QSize(16777215, 120))
        self.first_page_label.setObjectName("first_page_label")
        self.verticalLayout_3.addWidget(self.first_page_label)
        self.file_open_btn = QtWidgets.QPushButton(self.page_1)
        self.next_page_btn = QtWidgets.QPushButton(self.page_1)
        self.next_page_btn.setText("Обработать файл")
        self.next_page_btn.setMinimumSize(QtCore.QSize(100, 0))
        self.next_page_btn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.open_viewer = QtWidgets.QPushButton(self.page_1)
        self.open_viewer.setText("Просмотр данных")
        self.open_viewer.setMinimumSize(QtCore.QSize(100, 0))
        self.open_viewer.setMaximumSize(QtCore.QSize(100, 16777215))
        self.file_open_btn.setMinimumSize(QtCore.QSize(100, 0))
        self.file_open_btn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.file_open_btn.setObjectName("file_open_btn")
        self.hor_lay_ = QtWidgets.QHBoxLayout()
        self.hor_lay_.addWidget(self.file_open_btn)
        self.hor_lay_.addWidget(self.next_page_btn)
        self.hor_lay_.addWidget(self.open_viewer)
        self.verticalLayout_3.addLayout(self.hor_lay_)
        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.secon_label = QtWidgets.QLabel(self.page_2)
        self.secon_label.setObjectName("secon_label")
        self.verticalLayout_4.addWidget(self.secon_label)
        self.open_window_btn = QtWidgets.QPushButton()
        self.open_window_btn.setText("Просмотр данных")
        self.hor_lay = QtWidgets.QHBoxLayout()
        self.hor_lay.addWidget(self.open_window_btn)
        self.verticalLayout_4.addLayout(self.hor_lay)
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout_2.addWidget(self.stackedWidget)
        self.verticalLayout.addWidget(self.frame)
        self.file_open_btn.clicked.connect(self.open_file)
        self.open_window_btn.clicked.connect(self.open_table)
        self.next_page_btn.clicked.connect(self.get_txt_data)
        self.open_viewer.clicked.connect(self.open_table)
        self.window = Window
        self.path = ""
        self.next_page_btn.setEnabled(False)
        self.numbers = []

        self.retranslateUi(Window)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Window)


    def get_txt_data(self):
        with open(f"{self.path}", "r", encoding="utf-8") as f:
            data = f.read().strip()
            data = "".join(data).split()
            self.numbers = data.copy()
            self.proccess_file()
        
    
    def proccess_file(self):
        self.open_window_btn.setEnabled(True)
        self.stackedWidget.setCurrentIndex(1)
        self.window.close()
        thread = threading.Thread(
            target=main,
            args=(self.numbers,),
            daemon=True,
        )
        thread.start()
        thread.join()
        self.window.show()
    
        
    def open_table(self):
        import os
        os.startfile("Open DB.exe")
        self.window.close()
        
    
    def open_file(self):
        file_ = QFileDialog()
        file_.setNameFilter("Text files (*.txt)")
        if file_.exec():
            filenames = file_.selectedFiles()
            self.first_page_label.setText(filenames[0])
            self.first_page_label.setStyleSheet("font-size: 12pt;")
            self.first_page_label.setWordWrap(True)
            self.path = filenames[0]
            self.next_page_btn.setEnabled(True)
        

        

    def retranslateUi(self, Window):
        _translate = QtCore.QCoreApplication.translate
        Window.setWindowTitle(_translate("Window", "Проверка Государственного номера"))
        self.first_page_label.setText(_translate("Window", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Для продолжения, </span></p><p align=\"center\"><span style=\" font-size:12pt;\">выберите файл формата .txt</span></p></body></html>"))
        self.file_open_btn.setText(_translate("Window", "Открыть файл"))
        self.secon_label.setText(_translate("Window", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">База успешно обновлена,</span></p><p align=\"center\"><span style=\" font-size:12pt;\">нажмите кнопку, чтобы продолжить...</span></p></body></html>"))
   


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    window = Ui_Window()
    window.setupUi(widget)
    widget.show()
    sys.exit(app.exec())
