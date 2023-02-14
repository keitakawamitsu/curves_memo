#kmt_curves_memo_gui.py

import os
import sys

from maya import OpenMayaUI
from shiboken2 import wrapInstance
from PySide2.QtGui import*
from PySide2.QtCore import*
from PySide2.QtWidgets import*

from . import kmt_make_curves

def get_main_window():
    """Maya画面の後ろにいかせない"""

    mayaMainWindowPtr = OpenMayaUI.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr),QWidget)
    return mayaMainWindow

def close_child(app):
    """ ウィンドウの重複回避 """

    parent_list =  app.parent().children()
    for i in parent_list:
        if app.__class__.__name__ == i.__class__.__name__:
            i.close()

class MemoPad(QMainWindow):
    def __init__(self,parent=None):
        super(MemoPad, self).__init__(parent)
        close_child(self)
        self.mainGUI()
    
    def mainGUI(self):
        self.resize(400, 100)
        self.setWindowTitle('Memo pad')
        self.textEdit = QTextEdit(self)
        button = QPushButton(self.textEdit)
        button.setText("apply")
        button.clicked.connect(self.make_text_curves)

        self.text_h_layout = QHBoxLayout()
        self.text_h_layout.addWidget(self.textEdit)

        self.apply_h_layout = QHBoxLayout()
        self.apply_h_layout.addWidget(button)

        main_v_widget = QVBoxLayout()
        main_v_widget.addLayout(self.text_h_layout)
        main_v_widget.addLayout(self.apply_h_layout)

        self.widget = QWidget()
        self.widget.setLayout(main_v_widget)
        self.setCentralWidget(self.widget)
    
    def make_text_curves(self):
        text = self.textEdit.toPlainText()
        cv = kmt_make_curves.MakeCurves(text)
        cv.make_curves(text)


def main():
    mayaWindow=get_main_window()
    app = QApplication.instance()
    memoPad = MemoPad(mayaWindow)
    memoPad.show()
    #sys.exit()
    app.exec_()

if __name__ == "__main__":
    main()