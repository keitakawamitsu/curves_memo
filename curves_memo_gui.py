
import os
import sys
import subprocess
from maya import OpenMayaUI
from shiboken2 import wrapInstance
from PySide2.QtGui import*
from PySide2.QtCore import*
from PySide2.QtWidgets import*

def get_main_window():
    """Maya画面の後ろにいかせない"""

    mayaMainWindowPtr = OpenMayaUI.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr),QWidget)
    return mayaMainWindow


class MemoPad(QMainWindow):
    def __init__(self,parent=None):
        super(MemoPad, self).__init__(parent)
        self.mainGUI()
    
    def mainGUI(self):
        self.resize(400, 100)
        self.setWindowTitle('Memo pad')
        self.textEdit = QTextEdit(self)
        #self.setCentralWidget(self.textEdit)
        button = QPushButton(self.textEdit)
        button.setText("aa")
        button.clicked.connect(self.get_text)


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
    
    def get_text(self):
        a=self.textEdit.toPlainText()
        cmds.textCurves( f='Times-Roman', t=a )
        print(self.textEdit.toPlainText())


def main():
    a=get_main_window()
    app = QApplication.instance()
    memoPad = MemoPad(a)
    memoPad.show()
    sys.exit()
    app.exec_()

if __name__ == "__main__":
    main()