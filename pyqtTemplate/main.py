from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import hello

class ExampleApp(QtWidgets.QMainWindow, hello.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        
app = QApplication(sys.argv)
form = ExampleApp()
form.show()




def say():
    a = form.lineEdit.text()
    print("said",a)





def main():
    app.exec_()
    


if __name__ == '__main__':
    main()
