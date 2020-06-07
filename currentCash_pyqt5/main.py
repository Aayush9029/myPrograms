from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication

import sys
import layout
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import geckodriver_autoinstaller
from time import sleep

ublock = '/Users/aayushpokharel/Library/Application Support/Firefox/Profiles/m61m9jai.default-release-1588469903480/extensions/uBlock0@raymondhill.net.xpi'
url = "https://www.theglobeandmail.com/investing/markets/stocks/AC-T/"
url = "file:///Users/aayushpokharel/Desktop/stockmaker/index.html"

geckodriver_autoinstaller.install()  

options = webdriver.FirefoxOptions()
driver = webdriver.Firefox()
driver.install_addon(ublock, temporary=True)

driver.get(url)

def currentPrice():
    return driver.find_element_by_name("lastPrice").text


class ExampleApp(QtWidgets.QMainWindow, layout.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.save_btn.clicked.connect(self.getInfo)
        self.paid_price = 0
        self.num_of_stocks = 0
        
    
    def getInfo(self):
        self.number_of_stocks = self.num_stocks.text()
        self.paid_price = self.prev_price.text()
        self.relable()

        print(f"Number of stocks bought: {self.number_of_stocks}\nPrice Paid {self.paid_price}") 
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.relable)
        self.timer.start()


    def relable(self):
            net = float(currentPrice()) - float(self.paid_price)
            self.currentLabel.setText(str(round(net * int(self.number_of_stocks),2)))







def main(): 

    last_price = driver.find_element_by_name("lastPrice").text
    print("starting price was: ", last_price)

        
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()
    


if __name__ == '__main__':
    main()
    driver.quit()
