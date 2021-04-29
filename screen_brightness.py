import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QDialog,
                             QApplication, QSlider, QPushButton, QLabel, QHBoxLayout, QVBoxLayout)


class DisplayBrightness(QWidget):

    def __init__(self):
        super(DisplayBrightness, self).__init__()
        self.initUI()

    def initUI(self):
        # setting slider design
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 100)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(5)
        # apply last brightness data and connect slider
        self.saved_data = self.get_saved_data()
        self.slider_lbl = QLabel(str(self.saved_data))
        self.slider.setValue(self.saved_data)
        self.slider.valueChanged.connect(self.slider_changed)
        # connect screen activating button
        self.activate_btn = QPushButton('켜기', self)
        self.activate_btn.clicked.connect(self.gray_screen_show)
        # darkening screen setting
        self.gray_screen = QDialog()
        self.gray_screen.setWindowModality(Qt.NonModal)
        self.gray_screen.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowTransparentForInput)
        self.gray_screen.setAttribute(Qt.WA_ShowWithoutActivating)
        self.gray_screen.setAttribute(Qt.WA_TranslucentBackground)
        # button just to apply transparent full screen image (not working as button)
        self.gray_btn = QPushButton('', self.gray_screen)
        self.gray_btn.setGeometry(0, 0, 5000, 5000)
        # setting layout
        hbox_btn = QHBoxLayout()
        hbox_btn.addStretch(1)
        hbox_btn.addWidget(self.activate_btn)
        hbox_btn.addStretch(1)

        hbox_lbl = QHBoxLayout()
        hbox_lbl.addStretch(1)
        hbox_lbl.addWidget(self.slider_lbl)
        hbox_lbl.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_lbl)
        vbox.addWidget(self.slider)
        vbox.addStretch(1)
        vbox.addLayout(hbox_btn)

        self.setLayout(vbox)

        self.setWindowTitle('화면 밝기 조정기')
        self.setGeometry(300, 300, 300, 150)
        self.show()

    # getting last execution's brightness data
    def get_saved_data(self):
        import os

        saved_data = 0
        if os.path.exists('save.txt'):
            with open('save.txt', 'rt') as fin:
                try:
                    saved_data = int(fin.read())
                except Exception as read_error:
                    # when save.txt is written in none-number text
                    pass

        return saved_data

    # connect to label and adjust screen's transparency
    def slider_changed(self):
        self.slider_lbl.setText(str(self.slider.value()))

        if self.gray_screen.isVisible():
            self.gray_btn.setStyleSheet(f"background-color: rgba(0, 0, 0, {self.slider.value() * 255 / 100})")

    # change button's text and show/close screen
    def gray_screen_show(self):
        if self.gray_screen.isVisible():
            self.activate_btn.setText('켜기')
            self.gray_screen.close()
        else:
            self.activate_btn.setText('끄기')
            self.gray_btn.setStyleSheet(f"background-color: rgba(0, 0, 0, {self.slider.value() * 255 / 100})")
            self.gray_screen.show()

    # close screen together and save brightness data
    def closeEvent(self, event):
        self.gray_screen.close()
        self.save_data()

    def save_data(self):
        with open('save.txt', 'wt') as fout:
            fout.write(str(self.slider.value()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DisplayBrightness()
    ex.show()
    sys.exit(app.exec_())
