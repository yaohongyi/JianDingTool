#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import sys
import os
import base64
from picture.icon import img
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from file_operate import FileOperate
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

with open('tmp.ico', 'wb') as tmp:
    tmp.write(base64.b64decode(img))


class Client(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        '''窗口绘制'''
        self.setFixedSize(350, 120)
        self.setWindowTitle('鉴定版本切换工具_20200430')
        self.setWindowIcon(QtGui.QIcon('tmp.ico'))
        os.remove('tmp.ico')
        self.client_grid = QGridLayout(self)
        self.dev_model_label = QLabel('开发者模式：')
        self.on_rb = QRadioButton('打开', self)
        self.on_rb.setChecked(True)
        self.off_rb = QRadioButton('关闭', self)
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.off_rb, 0)
        self.button_group.addButton(self.on_rb, 1)
        self.edition_label = QLabel('请选择版本：')
        self.edition_combo_box = QComboBox()
        self.edition_combo_box.addItems(['基础版', '高级版', '专家版'])
        self.edition_combo_box.setCurrentIndex(2)
        self.log_info = QLabel()
        self.change_button = QPushButton('切换(F10)')
        self.change_button.setShortcut('F10')
        self.change_button.clicked.connect(self.change_edition)
        '''元素布局'''
        self.client_grid.addWidget(self.dev_model_label, 0, 0, 1, 1)
        self.dev_model_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft)
        self.client_grid.addWidget(self.off_rb, 0, 1, 1, 1)
        self.client_grid.addWidget(self.on_rb, 0, 2, 1, 1)
        self.client_grid.addWidget(self.edition_label, 1, 0, 1, 1)
        self.edition_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft)
        self.client_grid.addWidget(self.edition_combo_box, 1, 1, 1, 1)
        self.client_grid.addWidget(self.log_info, 2, 0, 1, 3)
        self.client_grid.addWidget(self.change_button, 3, 0, 3, 3)

    def get_edition_value(self):
        model_value = self.button_group.checkedId()
        edition_value = self.edition_combo_box.currentIndex()
        return model_value, edition_value

    def change_edition(self):
        model_value, edition_value = self.get_edition_value()
        self.file_operate_thread = FileOperate(model_value, edition_value)
        self.file_operate_thread.text.connect(self.print_log)
        self.file_operate_thread.start()

    def print_log(self, text):
        self.log_info.setText(text)
        self.log_info.setStyleSheet("color:blue")


def main():
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
