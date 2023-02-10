# coding:utf-8
import re
import unicodedata
from maya import cmds as cmds

class MakeCurves:
    def __init__(self,text):
        self.text = text
        self.tx = Text(self.text)

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
    
    def make_shape(self,cv_name,textCurvesNode):
        #cv_name,textCurvesNode = self.get_text()
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
        print(shape_list)

    def rename_transform(self,*arg):
        pas_text = self.tx.parsing()
        pattern = r'^[Text]{1,4}_(.*?)_\d{1,3}$'
        allNodes = cmds.ls(typ="transform")
        new_text =""
        for i in allNodes:#カーブ作った後のtransformノード調べて、matchする部分を取得
            a=re.search(pattern,i)
            if a:
                str = a.group(1)
                new_text = i.replace(str,pas_text)#パースされた文字と置き換え
                cmds.rename(i,new_text)
                break
            
            else:
                print(f"{i} is non match node")

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

    def main(self):
        #カーブ作る
        #if Mayaで使える文字列ですか？:
        #   使える文字列に変換する
        #if それはシーンの中にありますか？
        #   あったら文字列変更
        #   なかったらスルー
        #シェイプマージ
        #
        pass
    def make_curves(self,input_text):
       cv_name,textCurvesNode = cmds.textCurves( f='times-roman',t = input_text)#カーブの生成はこれくらいシンプルにしないとアカン
       print(cv_name)
       self.rename_transform()
       return cv_name,textCurvesNode


class Text:
    def __init__(self, text=""):
        self.text = text

    def parsing(self):
        """構文解析用。mayaが使えない文字はアンスコに変換する
        """
        print("-------in_text is --------")
        print(self.text)
        small_text = unicodedata.normalize('NFKC',self.text)
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
    
    def is_node(self,parsing_text):
        """パースされた文字を受け取り、その名前でScene内を探し、重複があったら変更用のフラグを返す
        """
        pas_name = parsing_text
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
                print(f"{pas_name}はないのでnode作ってOK")
                num = 0
                return num
    
    
    def rename_node(self,result):
        """Scene内のノードを探し、重複してたら新しい名前にして返す
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