from datetime import datetime

import requests
from PyQt5 import QtWidgets, QtCore
import clientui

class Window(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self, url):
        super().__init__()
        self.setupUi(self)

        self.url = url

        self.pushButton.pressed.connect(self.send_message)

        #запуск по таймеру(timer):
        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)

    def get_messages(self):
        try:
            response = requests.get(self.url + '/messages', params={'after': self.after})
        except:
            return
        response_data = response.json()

        for message in response_data['messages']:
            self.print_message(message)
            self.after = message['time']

    def print_message(self, message):
        time_dec = datetime.fromtimestamp(message['time'])
        time_dec = time_dec.strftime('%d/%m %H:%M')
        self.textBrowser.append(time_dec + ' ' + message['name'])
        self.textBrowser.append(message['text'])
        self.textBrowser.append('')

    def send_message(self):
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()

        try:
            response = requests.post(self.url + '/send', json=
            {
                'name': name,
                'text': text
            })
        except:
            self.textBrowser.append('Сервер временно недооступен')
            self.textBrowser.append('')
            return
        if response.status_code != 200:
            self.textBrowser.append('Поля ввода имени или текста не заполнены')
            self.textBrowser.append('')
            return

        self.textEdit.clear()

app = QtWidgets.QApplication([])
window = Window(url = 'http://127.0.0.1:5000')
window.show()
app.exec_()
