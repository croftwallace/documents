#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 14:16:56 2020

@author: wallace
"""

#from Pytrans import Pytrans
import codecs
import execjs
import requests
import os


class Pytrans():  
    def __init__(self):  
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072;       
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f"; 
     
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
    }; 
     
    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 
    """)  # 获取代码编译完成后的对象     
    def cd_num(self,text):  
        return self.ctx.call("TL",text)
    

# google translation
def google_translate(original_text):
    
    js = Pytrans()
    tk = js.cd_num(original_text)

    if len(original_text) > 4950:      
        print("Too long, string to translate must be less than 5000 characters long.")      
        return      
    param = {'tk': tk, 'q': original_text}  
    result = requests.get("""http://translate.google.cn/translate_a/single?client=webapp&sl=en
        &tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss
        &dt=t&clearbtn=1&otf=1&pc=1&ssel=0&tsel=0&kc=2""", params=param)
   
    trans = result.json()[0]
    ret = ''
    for i in range(len(trans)):
        line = trans[i][0]
        if line != None:
            ret += trans[i][0]

    return ret

#a= google_translate("hello，Input file will be translated, please be patient")
#print(a)
  
baseDir = os.path.dirname(os.path.abspath(__name__))
suffix = 'vtt'
subtitle_list = []

print(baseDir)

def find_en_subtitle(baseDir):
    if not os.path.isdir(baseDir):
        exit(-1)
    #得到文件夹下的所有文件名称
    for f in os.listdir(baseDir):
        file = baseDir + '/' + f
        if os.path.isfile(file):
            if f.endswith(suffix) and 'zh' not in f:
                print(f)
                subtitle_list.append(file)
        else:
            find_en_subtitle(file)
            
find_en_subtitle(baseDir)    


for file in subtitle_list:
    # deal origin text
    print(file)
    trasnlation_list = []
    zh_file = file.replace('/en','').replace(suffix,'zh.' + suffix)
    if os.path.exists(zh_file):
        print(zh_file + 'already exists')
        continue
    translate_file = open(zh_file, "w", encoding='utf_8_sig')
    with open(file,'r',encoding='utf_8_sig') as f:
        for element in f:
            #print(element)
            '''
            element = re.sub(r" &amp; ", "", element)
            element = re.sub(r".", " ", element)
            element = re.sub(r",", " ", element)
            '''
            #print(element)
            if element.strip().isdigit():
                #print(element + 'is a num')
                continue
                
            element = element.replace(" &amp; ", "")
            trasnlation_list.append(element)
    #print(trasnlation_list)
    
    count = 0
    # translate text
    for tl in trasnlation_list:
        #print(tl)
        if tl.isspace():
            #print('this is line break')
            translate_file.write('\n')
        elif '-->' in tl:
            translate_file.write(tl)
        else:
            translation = google_translate(tl)
            translation = translation.replace("。", " ")
            translation = translation.replace("，", " ")
            translate_file.write(translation + '\n')
    
            count += 1
            print('complete', '%.1f%%'%((count/len(trasnlation_list))*100))
            
    translate_file.close()
    
print('translate finished')

''' 
    translation = google_translate(tl)
    #translate_file.write(tl + '\t' + translation + '\n')
    translate_file.write(translation + '\n')
    print(translation)
    count += 1
    print('complete', '%.1f%%'%((count/len(trasnlation_list))*100))
'''