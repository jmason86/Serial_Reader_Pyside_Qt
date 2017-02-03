"""Call the GUI and attach it to functions."""
__author__ = "James Paul Mason"
__contact__ = "jmason86@gmail.com"

import sys
import logging
from PySide.QtGui import *
from PySide.QtCore import *
from ui_mainWindow import Ui_MainWindow
import connect_serial_decode_kiss
from PySide import QtCore, QtGui
import time

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.assignWidgets()
        self.log = self.createLog()
        self.show()
    
    def assignWidgets(self):
        self.button_connectSerial.clicked.connect(self.connecetSerialClicked)
        self.button_startRead.clicked.connect(self.startReadClicked)
        self.button_stopRead.clicked.connect(self.stopReadClicked)
        self.checkBox_saveLog.stateChanged.connect(self.saveLogToggled)
    
    def connecetSerialClicked(self):
        # Grab the port and baud rate from UI
        port = self.textEdit_serialPort.toPlainText()
        baudRate = self.textEdit_baudRate.toPlainText()
        
        # Connect to the serial port and test that it is readable
        connectedPort = connect_serial_decode_kiss.connect_serial_decode_kiss(port, baudRate, self.log)
        portReadable = connectedPort.testRead()
    
        # If port is readable, store the reference to it and update the GUI
        if portReadable:
            self.connectedPort = connectedPort
            self.label_connected.setText(QtGui.QApplication.translate("MainWindow", "Connected: Yes", None, QtGui.QApplication.UnicodeUTF8))
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Foreground, QColor(55, 195, 58))
            self.label_connected.setPalette(palette)

    def startReadClicked(self):
        # Update the GUI reading toggle
        self.label_reading.setText(QtGui.QApplication.translate("MainWindow", "Reading", None, QtGui.QApplication.UnicodeUTF8))
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground, QColor(55, 195, 58))
        self.label_reading.setPalette(palette)

        # Infinite loop to read the serial port and display the data in the GUI
        self.userStopped = False
        index = 0
        while(True):
            #    serialData = self.connectedPort.read()
            self.label_serialOutput.setText(str(index))
            index += 1
            time.sleep(0.05)
            QtGui.qApp.processEvents()
            if self.userStopped:
                break
            #self.label_serialOutput.setText(serialData)
    
    def stopReadClicked(self):
        self.userStopped = True
    
        # Update the GUI reading toggle
        self.label_reading.setText(QtGui.QApplication.translate("MainWindow", "Not Reading", None, QtGui.QApplication.UnicodeUTF8))
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground, QColor(242, 86, 77))
        self.label_reading.setPalette(palette)

    def saveLogToggled(self):
        if self.checkBox_saveLog.isChecked():
            self.label_savingToLogFile.setText("Saving to log file:" + ) # TODO: Pickup here. Also need to default with a filename on initialization. 

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
