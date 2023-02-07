# coding:utf-8
import re
import unicodedata
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


        def hoge(self):
            """構文解析用
            """
            text = "10F~44f"
            small_text = unicodedata.normalize('NFKC',text)
            new_list = []
            for i in small_text:
                """mayaが使えない文字はアンスコに変換する
                """
                if re.search("[0-9]+",i):
                    new_list.append(i)
                elif re.search("[a-zA-Z]+",i):
                    new_list.append(i)
        
                elif re.search("\W",i):
                    if i == "~":
                       _ = i.replace(i,"~")
                       new_list.append(_)
                    else:
                        _ = i.replace(i,"_")
                        new_list.append(_)
        
                elif re.compile('[\u3041-\u309F]+'):
                    print(i)
                    _ = i.replace(i,"_")
                    new_list.append(_)    
                else:
                    new_list.append(i)
        
            _re_text = "".join(new_list)
            print(_re_text)
    
            curves_text = cmds.textCurves( f='times-roman',t= _re_text)[0]
            result1 = re.split("_",curves_text)[1]
            new_curves_text = curves_text.replace(result1,_re_text)
            cmds.rename(curves_text,new_curves_text)


