# coding:utf-8
from maya import cmds as cmds

class Text:
    def __init__(self):
        pass

    def get_text(self,text):
        if text:
            cmds.textCurves( f='times-roman', t=text)
        else:
            cmds.warning(r"テキストを入力して下さい")
