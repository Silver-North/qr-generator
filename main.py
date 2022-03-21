#!/usr/bin/env python3


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from design import Ui_MainWindow
from sys import exit
from os import path, system
from time import sleep
from threading import Thread
from qrcode import make
from validators import url as check_url
from PIL import Image


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.patch = path.dirname(path.realpath(__file__))
        # self.setGeometry(900, 55, 400, 300)

        self.current_path = path.dirname(path.realpath(__file__))

        self.ui.toolButton_2.setIcon(QIcon(f'{self.current_path}/spinner.png'))
        self.ui.toolButton_3.setIcon(QIcon(f'{self.current_path}/diskette.png'))
        self.ui.toolButton.clicked.connect(self.getPathFile)
        self.ui.toolButton_2.clicked.connect(self.textQR)
        self.ui.toolButton_3.clicked.connect(self.saved)


    def generate(self, text):
        filename = 'qr.png'

        img = make(text)
        img.save(filename)


    def saved(self):
        text = self.ui.lineEdit_3.text()
        if text != '':
            system(f'mv {self.current_path}/qr.png {self.current_path}/saved/{text}.png')
        else:
            self.ui.lineEdit_3.setText("   Error..")
            self.ui.lineEdit_3.setStyleSheet('color: rgb(255, 0, 0); border: 1px solid rgb(255, 0, 0)')
            Thread(target = self.defSave).start()


    def defSave(self):
        sleep(5)
        self.ui.lineEdit_3.setText('')
        self.ui.lineEdit_3.setStyleSheet('color: rgb(0, 0, 0); border: 1px solid rgba(181, 178, 178, 0.6)')


    def getPathFile(self):
        file_path = QFileDialog.getOpenFileName()[0]
        name = file_path.split('/')[-1]
        print(name)
        self.ui.label_2.setText(name)
        system(f'cp {file_path} {self.current_path}')
        self.generate(f'{self.current_path}/{name}')
        self.loadImage()


    def loadImage(self):
        cube = 131
        img = Image.open(f'{self.current_path}/qr.png')
        resizing = img.resize((cube, cube), Image.ANTIALIAS)
        resizing.save('qr.png')
        pixmap = QPixmap(f'{self.current_path}/qr.png')
        self.ui.label_3.setPixmap(pixmap)


    def textQR(self):
        if self.ui.toolBox.currentIndex() == 0:
            text = self.ui.lineEdit.text()
            if text != "":
                self.generate(text)
            else:
                self.ui.lineEdit.setStyleSheet('color: rgb(255, 0, 0); border: 1px solid rgb(255, 0, 0)')
                self.ui.lineEdit.setText('    Write text..')
                Thread(target = self.pauseColorDefault).start()
        elif self.ui.toolBox.currentIndex() == 1:
            url = self.ui.lineEdit_2.text()
            if check_url(url):
                self.generate(url)
            else:
                self.ui.lineEdit_2.setText('   Write url..')
                self.ui.lineEdit_2.setStyleSheet('color: rgb(255, 0, 0); border: 1px solid rgb(255, 0, 0)')
                Thread(target = self.pauseColorDefault, args = (True,)).start()
        elif self.ui.toolBox.currentIndex() == 2:
            pass

        self.loadImage()


    def pauseColorDefault(self, flag=False):
        sleep(5)
        if flag:
            self.ui.lineEdit_2.setText('')
            self.ui.lineEdit_2.setStyleSheet('color: rgb(0,0,0); border: 1px solid rgba(181, 178, 178, 0.6)')
        else:
            self.ui.lineEdit.setText('')
            self.ui.lineEdit.setStyleSheet('color: rgb(0,0,0); border: 1px solid rgba(181, 178, 178, 0.6)')


# data = input("Write URL or other data:  ")
# factory = PymagingImage

# qr = QRCode(version=1, error_correction=constants.ERROR_CORRECT_L, box_size=100, border=4, image_factory=factory)

# qr.add_data(data)
# qr.make(fit=True)

# img = qr.make_image(fill_color="red", back_color="green")



app = QtWidgets.QApplication([])
application = mywindow()

application.show()

exit(app.exec())
