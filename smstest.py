import sys, serial, time
from PyQt5 import QtWidgets as QW
from sms import Ui_Form

class my_app(QW.QMainWindow):
    def __init__(self):   #, parent=None):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.start_SMS)

    def start_SMS(self):
        list_number = self.ui.plainTextEdit_1.toPlainText().split('\n')
        text_SMS = self.ui.plainTextEdit_2.toPlainText()
#        msg.decode('utf8').encode('cp1251')

        GSM = serial.Serial('COM4', 19200, timeout=5)
        time.sleep(3)
        GSM.write('AT\r')
        otvet = GSM.read()
        print(otvet)
        for number in list_number:
            print('Phone: {0} text: {1}'.format(number, text_SMS))
#            GSM.write(chr(26))
        GSM.close()


app = QW.QApplication(sys.argv)
window = my_app()
window.show()
app.exec_()
