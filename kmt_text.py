# coding:utf-8
import re
import unicodedata
from maya import cmds as cmds

class Text:
    def __init__(self):
        pass
    
    def is_node(self,input_text):
        allNodes = cmds.ls(typ="transform")
        pattern = r'_\d{1,3}$'#最後の文字が数字3桁ならTrue

        for node in allNodes:
            if input_text in node:
                num = re.search(pattern,node)
                if num:
                    num1=int(num[0][1:])
                    num1 += 1
                    print(num1)#最後インクリ
                    break
                    
                else:
                    print("処理終わらす")#シーン内に同じ名前はないので、入力された文字をそのまま使う



    def parsing(self,in_text):
        """構文解析用。mayaが使えない文字はアンスコに変換する
        """
        print("-------in_text is --------")
        print(in_text)
        small_text = unicodedata.normalize('NFKC',in_text)
        new_list = []

        print("-------small_text is --------")
        print(small_text)

        for i in small_text:
            if re.search("[0-9]+",i):
                new_list.append(i)
            elif re.search("[a-zA-Z]+",i):
                new_list.append(i)
        
            elif re.search("\W",i):
                _ = i.replace(i,"_")
                new_list.append(_)

            elif re.compile('[\u3041-\u309F]+'):
                _ = i.replace(i,"_")
                new_list.append(_)    
            else:
                new_list.append(i)
        
        self.response = "".join(new_list)
        
        print("------------------parsing self.response is ------------------")
        print(self.response)
        return self.response

    def get_text(self,text):
        small_text = unicodedata.normalize('NFKC',text)

        parsing_text = self.parsing(text)

        if text:
            cv_name,textCurvesNode = cmds.textCurves( f='times-roman',t=small_text)
        else:
            cmds.warning(r"テキストを入力して下さい")

        print("-------get_text cv_name is -----------------")
        print(cv_name)

        result = re.split("_",cv_name)[1]

        print("-----------get_text result is --------")
        print(result)
        
        new_curves_text = cv_name.replace(result,parsing_text)
        print("---------------- new_curves_text is ----------------------")
        print(new_curves_text)
        cmds.rename(cv_name,new_curves_text)
        
        return new_curves_text,textCurvesNode
    
    def make_shape(self,get_text):
        cv_name,textCurvesNode = self.get_text(get_text)
        print("----------- cv_name is --------")
        print(cv_name)

        cv_shape = cmds.ls(cmds.listConnections(textCurvesNode,sh=1),typ="shape")
        shape_list = []
        for i in cv_shape:
            new_sh_name = i.replace("curve",cv_name+"_")
            name = cmds.rename(i,new_sh_name)
            shape_list.append(name)

        cmds.delete(textCurvesNode)
        cmds.makeIdentity(cv_name,a=1,t=1)
        shape_list.append(cv_name)
        cmds.parent(shape_list,r=1,s=1)
        cmds.delete(cmds.listRelatives(cv_name,typ="transform"))


