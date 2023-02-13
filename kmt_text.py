# coding:utf-8
import re
import unicodedata
from maya import cmds as cmds

print("--------- import MakeCurves ---------")

class MakeCurves:
    def __init__(self,text):
        """
        """
        self.text = text
        self.tx = Text(self.text)
    
    def make_shape(self,cv_name,textCurvesNode):
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

    
    def make_curves(self,input_text):
        pas_text = self.tx.parsing()
        result = self.tx.is_node(pas_text)

        if result:
            new_name = self.tx.rename_node(result)
            cv_name,textCurvesNode = cmds.textCurves( f='times-roman',t = input_text)
            renamed_name = cmds.rename(cv_name,new_name)

        else:

            cv_name,textCurvesNode = cmds.textCurves( f='times-roman',t = input_text)#カーブの生成はこれくらいシンプルにしないとアカン
            pattern = r'^[Text]{1,4}_(.*?)_\d{1,3}$'
            a = re.search(pattern,cv_name)
            str = a.group(1)

            str = "_"+ str +"_"
            pas_text = "_" + pas_text +"_"
            new_name = cv_name.replace(str,pas_text)#パースされた文字と置き換え
            
            renamed_name = cmds.rename(cv_name,new_name)

        self.make_shape(renamed_name,textCurvesNode)
        cmds.select(renamed_name)
    

class Text:
    def __init__(self, text=""):
        self.text = text

    def parsing(self):
        """構文解析用。mayaが使えない文字はアンスコに、日本語はローマ字に変換する
        """
        small_text = unicodedata.normalize('NFKC',self.text)
        new_list = []

        for i in small_text:
            if re.search("[0-9]+",i):
                new_list.append(i)

            elif re.search("[a-zA-Z]+",i):
                new_list.append(i)
        
            elif re.search("\W",i):
                _ = i.replace(i,"_")
                new_list.append(_)

            elif re.findall(r"[\u3041-\u3093\u30A1-\u30F6]",i):
                _ = self.replace_text(i)#日本語をローマ字
                new_list.append(_)

            elif re.compile('[\u3041-\u309F]+'):
                _ = i.replace(i,"_")
                new_list.append(_)    

            else:
                new_list.append(i)
        
        self.response = "".join(new_list)
        
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
                    num = 1
                    return num
            else:
                num = 0
                return num
    
    
    def rename_node(self,result):
        """Scene内のノードを探し、重複してたら新しい名前にして返す
        """
        if result:
            b = re.search('[0-9]{1,3}$',self.node)
            num = int(b.group(0))
            num += 1

            c = re.search(r'(.*?)\d{1,3}$',self.node)
            self.new_name = c.group(1)+str(num)
            return self.new_name

        else:
            pattern = r'^[a-zA-Z]{1,4}_(.*?)_\d{1,3}$'#先頭が1~4文字以内のアルファベット、最後が1~3桁の数字、真ん中はなんでもOK
            c = re.search(pattern,self.node)
            return c.group(1)

    
    def replace_text(self,text):
        """日本語をローマ字に置き換える
        """
        pattern = r"[\u3041-\u3093\u30A1-\u30F6]"
        result = re.findall(pattern, text)
        if result:
            # 平仮名とカタカタを英語に置き換える辞書
            japanese_dict = {
                'ぁ': 'a', 'あ': 'a', 'ぃ': 'i', 'い': 'i', 'ぅ': 'u', 'う': 'u',
                'ぇ': 'e', 'え': 'e', 'ぉ': 'o', 'お': 'o', 'か': 'ka', 'が': 'ga',
                'き': 'ki', 'ぎ': 'gi', 'く': 'ku', 'ぐ': 'gu', 'け': 'ke', 'げ': 'ge',
                'こ': 'ko', 'ご': 'go', 'さ': 'sa', 'ざ': 'za', 'し': 'shi', 'じ': 'ji',
                'す': 'su', 'ず': 'zu', 'せ': 'se', 'ぜ': 'ze', 'そ': 'so', 'ぞ': 'zo',
                'た': 'ta', 'だ': 'da', 'ち': 'chi', 'ぢ': 'ji', 'っ': 'tsu', 'つ': 'tsu',
                'づ': 'zu', 'て': 'te', 'で': 'de', 'と': 'to', 'ど': 'do', 'な': 'na',
                'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no', 'は': 'ha', 'ば': 'ba',
                'ぱ': 'pa', 'ひ': 'hi', 'び': 'bi', 'ぴ': 'pi', 'ふ': 'fu', 'ぶ': 'bu',
                'ぷ': 'pu', 'へ': 'he', 'べ': 'be', 'ぺ': 'pe', 'ほ': 'ho', 'ぼ': 'bo',
                'ぽ': 'po', 'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
                'ゃ': 'ya', 'や': 'ya', 'ゅ': 'yu', 'ゆ': 'yu', 'ょ': 'yo', 'よ': 'yo',
                'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro', 'ゎ': 'wa',
                'わ': 'wa', 'ゐ': 'i', 'ゑ': 'e', 'を': 'wo', 'ん': 'n', 'ァ': 'a',
                'ア': 'a', 'ィ': 'i', 'イ': 'i', 'ゥ': 'u', 'ウ': 'u', 'ェ': 'e',
                'エ': 'e', 'ォ': 'o', 'オ': 'o', 'カ': 'ka', 'ガ': 'ga', 'キ': 'ki',
                'ギ': 'gi', 'ク': 'ku', 'グ': 'gu', 'ケ': 'ke', 'ゲ': 'ge', 'コ': 'ko',
                'ゴ': 'go', 'サ': 'sa', 'ザ': 'za', 'シ': 'shi', 'ジ': 'ji', 'ス': 'su',
                'ズ': 'zu', 'セ': 'se', 'ゼ': 'ze', 'ソ': 'so', 'ゾ': 'zo', 'タ': 'ta',
                'ダ': 'da', 'チ': 'chi', 'ヂ': 'ji', 'ッ': 'tsu', 'ツ': 'tsu', 'ヅ': 'zu',
                'テ': 'te', 'デ': 'de', 'ト': 'to', 'ド': 'do', 'ナ': 'na', 'ニ': 'ni',
                'ヌ': 'nu', 'ネ': 'ne', 'ノ': 'no', 'ハ': 'ha', 'バ': 'ba', 'パ': 'pa',
                'ヒ': 'hi', 'ビ': 'bi', 'ピ': 'pi', 'フ': 'fu', 'ブ': 'bu'
                }
    
            for i in result:
                str = i.replace(i, japanese_dict[i])
        else:
            str="None"
        
        return str
    
