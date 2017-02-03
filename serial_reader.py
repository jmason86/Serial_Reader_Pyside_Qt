import sys
import logging
from PySide.QtGui import *
from PySide.QtCore import *
from ui_mainWindow import Ui_MainWindow
import connect_serial_decode_kiss
from PySide import QtCore, QtGui

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.assignWidgets()
        self.log = self.createLog()
        self.show()
    
    def assignWidgets(self):
        self.button_connectSerial.clicked.connect(self.connecetSerialPushed)
    
    def connecetSerialPushed(self):
        # Grab the port and baud rate from UI
        port = self.textEdit_serialPort.toPlainText()
        baudRate = self.textEdit_baudRate.toPlainText()
        
        # Connect to the serial port and test that it is readable
        connectedPort = connect_serial_decode_kiss.connect_serial_decode_kiss(port, baudRate, self.log)
        portReadable = connectedPort.testRead()
    
        # Update GUI with result of serial read test
        if portReadable:
            self.label_connected.setText(QtGui.QApplication.translate("MainWindow", "Connected: Yes", None, QtGui.QApplication.UnicodeUTF8))
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Foreground, QColor(55,195, 58))
            self.label_connected.setPalette(palette)

    def createLog(self):
        log = logging.getLogger('serial_reader')
        handler = logging.FileHandler('log/serial_reader.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)
        return log

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit( ret )
