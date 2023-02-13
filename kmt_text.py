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

    
    def make_curves(self,input_text):
        pas_text = self.tx.parsing()
        result = self.tx.is_node(pas_text)

        if result:
            print("ある---------------")
            new_name = self.tx.rename_node(result)
            cv_name,textCurvesNode = cmds.textCurves( f='times-roman',t = input_text)
            renamed_name = cmds.rename(cv_name,new_name)
            print(f"{renamed_name}")

        else:
            print("node ない場合の処理--------------------------------")

            cv_name,textCurvesNode = cmds.textCurves( f='times-roman',t = input_text)#カーブの生成はこれくらいシンプルにしないとアカン
            print(f"{cv_name} curves作った--------------------------------")
            pattern = r'^[Text]{1,4}_(.*?)_\d{1,3}$'
            a = re.search(pattern,cv_name)
            str = a.group(1)

            str = "_"+ str +"_"
            pas_text = "_" + pas_text +"_"
            new_name = cv_name.replace(str,pas_text)#パースされた文字と置き換え
            
            renamed_name = cmds.rename(cv_name,new_name)

            print(f"{renamed_name}")
        
        self.make_shape(renamed_name,textCurvesNode)
        cmds.select(renamed_name)
    

class Text:
    def __init__(self, text=""):
        self.text = text

    def parsing(self):
        """構文解析用。mayaが使えない文字はアンスコに、日本語はローマ字に変換する
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

            elif re.findall(r"[\u3041-\u3093\u30A1-\u30F6]",i):
                _ = self.convert_to_english(i)#日本語をローマ字
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
    
            #list = []
            for i in result:
                str = i.replace(i, japanese_dict[i])
                #list.append(str)
            #response = "".join(list)
        else:
            str="None"
        
        return str
    

    def convert_to_english(self,string):
        hiragana_dict = {'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
                            'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
                            'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
                            'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
                            'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
                            'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
                            'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
                            'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
                            'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
                            'わ': 'wa', 'を': 'wo', 'ん': 'n',
                            'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
                            'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
                            'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
                            'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
                            'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po'}

        katakana_dict = {'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o',
                            'カ': 'ka', 'キ': 'ki', 'ク': 'ku', 'ケ': 'ke', 'コ': 'ko',
                            'サ': 'sa', 'シ': 'shi', 'ス': 'su', 'セ': 'se', 'ソ': 'so',
                            'タ': 'ta', 'チ': 'chi', 'ツ': 'tsu', 'テ': 'te', 'ト': 'to',
                            'ナ': 'na', 'ニ': 'ni', 'ヌ': 'nu', 'ネ': 'ne', 'ノ': 'no',
                            'ハ': 'ha', 'ヒ': 'hi', 'フ': 'fu', 'ヘ': 'he', 'ホ':'ho',
                            'マ': 'ma', 'ミ': 'mi', 'ム': 'mu', 'メ': 'me', 'モ': 'mo',
                            'ヤ': 'ya', 'ユ': 'yu', 'ヨ': 'yo',
                            'ラ': 'ra', 'リ': 'ri', 'ル': 'ru', 'レ': 're', 'ロ': 'ro',
                            'ワ': 'wa', 'ヲ': 'wo', 'ン': 'n',
                            'ガ': 'ga', 'ギ': 'gi', 'グ': 'gu', 'ゲ': 'ge', 'ゴ': 'go',
                            'ザ': 'za', 'ジ': 'ji', 'ズ': 'zu', 'ゼ': 'ze', 'ゾ': 'zo',
                            'ダ': 'da', 'ヂ': 'ji', 'ヅ': 'zu', 'デ': 'de', 'ド': 'do',
                            'バ': 'ba', 'ビ': 'bi', 'ブ': 'bu', 'ベ': 'be', 'ボ': 'bo',
                            'パ': 'pa', 'ピ': 'pi', 'プ': 'pu', 'ペ': 'pe', 'ポ': 'po'}

        pattern = re.compile('[ぁ-ゟ゠-ヿ]+')
        match_list = pattern.findall(string)
    
        for match in match_list:
            for char in match:
                if char in hiragana_dict:
                    string = string.replace(char, hiragana_dict[char])
                elif char in katakana_dict:
                    string = string.replace(char, katakana_dict[char])
        return string
