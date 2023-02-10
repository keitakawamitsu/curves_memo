# coding:utf-8
import re
import unicodedata
from maya import cmds as cmds

class Text:
    def __init__(self,text):
        self.text = text
        pass

    def get_text(self):
        small_text = unicodedata.normalize('NFKC',self.text)

        parsing_text = self.parsing(self.text)

        if self.text:
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

        result = self.is_node()
        if result:
            new_curves_text=self.rename_node(result)
        else:
            pass

        cmds.rename(cv_name,new_curves_text)
        
        return new_curves_text,textCurvesNode
    
    def make_shape(self):
        cv_name,textCurvesNode = self.get_text()
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

    def is_node(self):
        pas_name = self.parsing(self.text)
        allNodes = cmds.ls(typ="transform")
        pattern = r'^[a-zA-Z]{1,4}_(.*?)_\d{1,3}$'#先頭が1~4文字以内のアルファベット、最後が1~3桁の数字、真ん中はなんでもOK
    
        for self.node in allNodes:
            a=re.search(pattern,self.node)
            if a:
                match_name = a.group(1)
                if match_name == pas_name:

                    print(f"{pas_name}はSceneにあるので違う名前にして{pas_name}を作る")
                    num = 1
                    return num
            else:
                print(f"{pas_name}はないのでnode作る")
                num = 0
                return num

    def rename_node(self,result):
        """Scene内のノードを探して、重複してたら新しい名前を返す
        """
        #result = self.is_node()
        if result:
            b = re.search('[0-9]{1,3}$',self.node)
            num = int(b.group(0))
            num += 1

            c = re.search(r'(.*?)\d{1,3}$',self.node)
            self.new_name = c.group(1)+str(num)
            return self.new_name

        else:
            print("普通にnode作る")
            return 0
            #self.get_text(self.text)

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
