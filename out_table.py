from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon
from database import Database   

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(603, 576)
        Form.setWindowIcon(QIcon('logo.png'))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.frame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 563, 487))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3.addLayout(self.verticalLayout_4)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addWidget(self.frame_2)
        self.save_btn = QtWidgets.QPushButton(self.frame_2)
        self.save_btn.setText("Сохранить")
        self.horizontalLayout.addWidget(self.save_btn)
        self.save_btn.clicked.connect(self.save_data)

        self.out_data()
        self.pushButton_2.clicked.connect(Form.close)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
        
    def out_data(self):
        db = Database()
        data = db.get_data(status="un_checked")
        if len(data) > 0:
            for i in range(len(data)):
                label = QtWidgets.QLabel(f"{data[i][0]}")
                label.setMinimumSize(QtCore.QSize(100, 30))
                label.setMaximumSize(QtCore.QSize(100, 30))
                label.setStyleSheet("font-size: 12pt;")
                if data[i][1] == "ТС эксплуатируется инвалидом или используется для перевозки инвалида":
                    label_2 = QtWidgets.QLabel()
                    label_2.setPixmap(QtGui.QPixmap(':/s/accept.png'))
                    label_2.setScaledContents(True)
                    label_2.setMinimumSize(QtCore.QSize(30, 30))
                    label_2.setMaximumSize(QtCore.QSize(30, 30))
                else:
                    label_2 = QtWidgets.QLabel()
                    label_2.setPixmap(QtGui.QPixmap(':/s/cross.png'))
                    label_2.setScaledContents(True)
                    label_2.setMinimumSize(QtCore.QSize(30, 30))
                    label_2.setMaximumSize(QtCore.QSize(30, 30))
                hor_layout = QtWidgets.QHBoxLayout()
                hor_layout.addWidget(label)
                hor_layout.addWidget(label_2)
                line = QtWidgets.QLineEdit()
                line.setMinimumSize(QtCore.QSize(200, 20))
                line.setMaximumSize(QtCore.QSize(200, 20))
                line.setPlaceholderText("Комментарий")
                if data[i][2] != "" and data[i][2] is not None:
                    line.setText(str(data[i][2]))
                line.setAlignment(QtCore.Qt.AlignCenter)
                hor_layout.addWidget(line)
                self.verticalLayout_4.addLayout(hor_layout)
                
                
    def save_data(self):
        db = Database()
        lines = self.scrollArea.findChildren(QtWidgets.QLineEdit)
        nums = self.scrollArea.findChildren(QtWidgets.QLabel)
        nums = [i.text().strip() for i in nums]
        nums = [i for i in nums if i != ""]
        for i in range(len(nums)):
            db.insert_comment(number=str(nums[i]), comment=str(lines[i].text()))
            
    
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Просмотр базы данных"))
        self.pushButton_2.setText(_translate("Form", "Закрыть"))
import res

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

