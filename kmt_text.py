# coding:utf-8
from maya import cmds as cmds

class Text:
    def __init__(self):
        pass

    def get_text(self,text):
        if text:
            self.cv_name = cmds.textCurves( f='times-roman',t=text)
        else:
            cmds.warning(r"テキストを入力して下さい")

        return self.cv_name
    
    def make_shape(self,get_text):
        shape_name = self.get_text(get_text)[0]
        _shape = cmds.duplicate(shape_name)[0]
    
        cmds.delete(shape_name)
        cmds.makeIdentity(_shape,a=1,t=1)
        cmds.select(_shape,hi=1)
        sh = cmds.listRelatives(s=1)
        trans = cmds.listRelatives(typ="transform")
    
        shape_list = []
        for i in sh:
            new_sh_name = i.replace("curve",_shape+"_")
            name = cmds.rename(i,new_sh_name)
            shape_list.append(name)
    
        shape_list.append(_shape)
        cmds.parent(shape_list,r=1,s=1)
        cmds.delete(trans)
        cmds.rename(_shape,shape_name)