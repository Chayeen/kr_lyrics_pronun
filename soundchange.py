#coding:utf-8  

# 感觉需要先对歌词过滤一下，有些歌词可能输入的格式就不太好，防御性编程
import codecs  
import glob  
import codecs  
import os
import re
import csv
import pdb

# vowels and consonants
first_parts = ("ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ")  
second_parts =("ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅗㅏ", "ㅗㅐ", "ㅗㅣ", "ㅛ", "ㅜ", "ㅜㅓ", "ㅜㅔ", "ㅜㅣ", "ㅠ", "ㅡ", "ㅡㅣ", "ㅣ")  
third_parts = ("", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ")  
# first_parts_yin = ("k/g", "gg", "n","t/d","dd","l","m","p/b","bb","s(x)","ss(xx)","","c(j)/j","jj","C(q)","K","T","P","h")
# second_parts_yin =("a", "ae", "ya", "yae", "eo", "e", "yeo", "ye", "o", "wa", "wae", "oe", "yo", "u", "wo", "we", "wi", "yu", "eu", "ui", "i")  
# third_parts_yin = ("", "g", "g", "g/d", "n", "n/d", "n/h", "d", "l", "g/l", "m/l", "l/b", "l/d", "l/d", "b/l", "l/h", "m", "b", "b/d", "d", "d", "ng", "d", "d", "g", "d", "b", "d")  
def divide_korean(temp_string):  
    temp_string_value = ord(temp_string)  
    part_1 = (temp_string_value - 44032) // 588  
    part_2 = (temp_string_value - 44032 - part_1 * 588) // 28  
    part_3 = (temp_string_value - 44032 ) % 28  
    return first_parts[part_1] + second_parts[part_2] + third_parts[part_3]

def double2single(double3):
    if double3 == "ㄲ":
        return "ㄱ"+ "ㄱ"
    elif double3 == "ㄳ":
        return "ㄱ" + "ㅅ"
    elif double3 == "ㄵ":
        return "ㄴ" + "ㅈ"
    elif double3 == "ㄶ":
        return "ㄴ" + "ㅎ"
    elif double3 == "ㄺ":
        return "ㄹ" + "ㄱ"
    elif double3 == "ㄻ":
        return "ㄹ" + "ㅁ"
    elif double3 == "ㄼ":
        return "ㄹ" + "ㅂ"
    elif double3 == "ㄽ":
        return "ㄹ" + "ㅅ"
    elif double3 == "ㄾ":
        return "ㄹ" + "ㅌ"
    elif double3 == "ㄿ":
        return "ㄹ" + "ㅍ"
    elif double3 == "ㅀ":
        return "ㄹ" + "ㅎ"
    elif double3 == "ㅄ":
        return "ㅂ" + "ㅅ"
    elif double3 == "ㅆ":
        return "ㅅ" + "ㅅ"
    else:
        print("input error, double3 must be in [ 'ㄲ', 'ㄳ',  'ㄵ', 'ㄶ',  'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅄ', 'ㅆ']")
        # return double3

def tight(single):
    if single == "ㄱ":
        return "ㄲ"
    elif single == "ㄷ":
        return "ㄸ"
    elif single == "ㅂ":
        return "ㅃ"
    elif single == "ㅅ":
        return "ㅆ"
    elif single == "ㅈ":
        return "ㅉ"
    else:
        print("input error, tight must be in ['ㄱ','ㄷ','ㅂ','ㅅ','ㅈ']")
        # return single

def palatalize(single):
    if single == "ㄷ":
        return "ㅈ"
    elif single == "ㅌ":
        return "ㅊ"
    else:
        print("input error, palatalize must be in ['ㄷ','ㅌ']")
        # return single

def aspirate(single):
    if single == "ㄱ":
        return "ㅋ"
    elif single == "ㄷ":
        return "ㅌ"
    elif single == "ㅈ":
        return "ㅊ"
    elif single == "ㅂ":
        return "ㅍ"
    else:
        print("input error, aspirate must be in ['ㄱ','ㄷ','ㅈ','ㅂ']")
        # return single

def list2str(ls):
    tmp = ""
    for x in ls:
        tmp = x + '|' + tmp
    tmp = tmp[:-1]
    # print(tmp)
    return tmp


def necessary_re_compile(rels,repldic):
# [必须规则]单收音连音化
    former= ["ㄱ","ㄴ","ㄷ","ㄹ","ㅁ","ㅂ","ㅅ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ"]
    later = "ㅇ"
    for x in former:
            rels.append(re.compile(x+'-'+later))
            repldic[re.compile(x+'-'+later)] = '-'+x
# [必须规则]ㅎ的脱落现象
    former = "ㅎ"
    later = "ㅇ"
    rels.append(re.compile(former+'-'+later))
    repldic[re.compile(former+'-'+later)] = '-'+later
# [必须规则]双收音连音化
    former = ["ㄲ","ㄵ","ㄺ","ㄻ","ㄼ","ㄾ","ㄿ"]
    later = "ㅇ"
    for x in former:
            rels.append(re.compile(x+'-'+later))
            doubledivide = double2single(x)
            repldic[re.compile(x+'-'+later)] = doubledivide[0]+'-'+doubledivide[1]
# [必须规则]结合ㅎ脱落和单收音连音
    former = ["ㄶ","ㅀ"]
    for x in former:
            rels.append(re.compile(x+'-'+later))
            doubledivide = double2single(x)
            repldic[re.compile(x+'-'+later)] = '-'+doubledivide[0]
# [必须规则] ㅅ连音需紧音化
    former = ["ㄳ","ㄽ","ㅄ","ㅆ"]
    for x in former:
            rels.append(re.compile(x+'-'+later))
            doubledivide = double2single(x)
            repldic[re.compile(x+'-'+later)] = doubledivide[0]+'-'+tight(doubledivide[1])

# [必须规则]收音鼻音化
    former = ["ㄱ","ㅋ","ㄲ","ㄺ","ㄳ"]
    later = ["ㄴ","ㅁ"]
    for y in later:
        # pa_tmp = ""
        # for x in former:
        #     pa_tmp = pa_tmp+ '|'+x
        # pa_tmp = pa_tmp[:-1]
        pa_tmp = list2str(former)
        # print(pa_tmp)
        rels.append(re.compile('['+pa_tmp+']'+'-'+y))
        repldic[re.compile('['+pa_tmp+']'+'-'+y)] = 'ㅇ'+'-'+y
    former = ["ㄷ","ㅌ","ㅅ","ㅈ","ㅊ","ㅆ","ㅎ"]
    for y in later:
        # pa_tmp = ""
        # for x in former:
        #     pa_tmp = pa_tmp+ '|'+x
        # pa_tmp = pa_tmp[:-1]
        pa_tmp = list2str(former)
        rels.append(re.compile('['+pa_tmp+']'+'-'+y))
        repldic[re.compile('['+pa_tmp+']'+'-'+y)] = 'ㄴ'+'-'+y
    former = ["ㅂ","ㅍ","ㅄ","ㄿ"]
    for y in later:
        # pa_tmp = ""
        # for x in former:
        #     pa_tmp = pa_tmp+ '|'+x
        # pa_tmp = pa_tmp[:-1]
        pa_tmp = list2str(former)
        rels.append(re.compile('['+pa_tmp+']'+'-'+y))
        repldic[re.compile('['+pa_tmp+']'+'-'+y)] = 'ㅁ'+'-'+y
# [必须规则]阻塞音紧音化
    former = ["ㄱ","ㅋ","ㄲ","ㄺ","ㄳ","ㄷ","ㅌ","ㅅ","ㅈ","ㅊ","ㅆ","ㅂ","ㅍ","ㅄ","ㄿ"]
    later = ["ㄱ","ㄷ","ㅂ","ㅅ","ㅈ"]
    for x in former:
        for y in later:
            rels.append(re.compile(x+'-'+y))
            repldic[re.compile(x+'-'+y)] = x+'-'+ tight(y)
# [必须规则]ㅎㅅ相遇
    former = ["ㅎ","ㄶ","ㅀ"]
    later = ["ㅅ"]
    for x in former:
        for y in later:
            rels.append(re.compile(x+'-'+y))
            if x == "ㅎ":
                repldic[re.compile(x+'-'+y)] = '-'+ tight(y)
            else:
                doubledivide = double2single(x)
                repldic[re.compile(x+'-'+y)] = doubledivide[0]+'-'+ tight(y)
# [必须规则]ㅎ在前送气化
    former = ["ㅎ","ㄶ","ㅀ"]
    later = ["ㄱ","ㄷ","ㅈ"]
    for x in former:
        for y in later:
            rels.append(re.compile(x+'-'+y))
            # repldic[re.compile(x+'-'+y)] = x+'-'+ aspirate(y)
            if x == "ㅎ":
                repldic[re.compile(x+'-'+y)] = '-'+ aspirate(y)
            else:
                doubledivide = double2single(x)
                repldic[re.compile(x+'-'+y)] = doubledivide[0]+'-'+ aspirate(y)
# [必须规则]ㅎ在后送气化,"ㄳ""ㅆ","ㅄ",
    former = ["ㄱ","ㄲ","ㄺ"]
    later = "ㅎ"
    for x in former:
            rels.append(re.compile(x+'-'+later))
            if x == "ㄱ":
                repldic[re.compile(x+'-'+later)] = '-'+ aspirate("ㄱ")
            else:
                doubledivide = double2single(x)
                repldic[re.compile(x+'-'+later)] = doubledivide[0]+'-'+ aspirate("ㄱ")
    # pa_tmp = list2str(former)
    # rels.append(re.compile('['+pa_tmp+']'+'-'+later))
    # repldic[re.compile('['+pa_tmp+']'+'-'+later)] = aspirate("ㄱ")+'-'+later

    former = ["ㄷ","ㅅ","ㅈ","ㅊ","ㅌ"]
    for x in former:
            rels.append(re.compile(x+'-'+later))
            repldic[re.compile(x+'-'+later)] = '-'+ aspirate("ㄷ")
    # pa_tmp = list2str(former)
    # rels.append(re.compile('['+pa_tmp+']'+'-'+later))
    # repldic[re.compile('['+pa_tmp+']'+'-'+later)] = '-'+aspirate("ㄷ")

    former= ["ㅂ","ㄿ"]
    for x in former:
            rels.append(re.compile(x+'-'+later))
            if x == "ㅂ":
                repldic[re.compile(x+'-'+later)] = '-'+ aspirate("ㅂ")
            else:
                doubledivide = double2single(x)
                repldic[re.compile(x+'-'+later)] = doubledivide[0]+'-'+ aspirate("ㅂ")
    # pa_tmp = list2str(former)
    # rels.append(re.compile('['+pa_tmp+']'+'-'+later))
    # repldic[re.compile('['+pa_tmp+']'+'-'+later)] = aspirate("ㅂ")+'-'+later

def divide_kr_line(inter_line):
    divided_line = ""
    for i in range(0, len(inter_line)):
        if inter_line[i] >= u'\uAC00' and inter_line[i] <= u'\uD7AF':  
            divided_line = divided_line + divide_korean(inter_line[i]) + '-'
        elif inter_line[i] ==' ':
            if len(divided_line) < 1:
                divided_line = inter_line[i]
            elif divided_line[-1] == '-':
                divided_line = divided_line[:-1] + '|'
            else:
                divided_line = divided_line + '|'
        elif inter_line[i] == "\n":
            divided_line = divided_line + "\n"
            break
        else :  
            divided_line = divided_line  + inter_line[i]
    return divided_line

def inter_kr_line(divided_line):
    tmp_word = ""
    inter_word  = ""
    inter_line = "["
    for i in range(0, len(divided_line)) :
        if divided_line[i] not in first_parts and divided_line[i] not in second_parts and divided_line[i] not in third_parts and divided_line[i] != '-' and divided_line[i] !='|' and divided_line[i] != '\n':
            inter_line = inter_line + divided_line[i]
            continue
        else:
            if divided_line[i] != '-' and divided_line[i] !='|' and divided_line[i] != '\n':
                tmp_word = tmp_word + divided_line[i]
            elif divided_line[i] == '-'  or divided_line[i] =='|' or divided_line[i] == '\n':
                if len(tmp_word)  == 2 :
                    inter_word = chr(first_parts.index(tmp_word[0])*588+second_parts.index(tmp_word[1])*28+44032)
                elif len(tmp_word) == 3 :
                    if tmp_word[2] in third_parts:
                        inter_word = chr(first_parts.index(tmp_word[0])*588+second_parts.index(tmp_word[1])*28+third_parts.index(tmp_word[2])+44032)
                    elif tmp_word[2] in second_parts:
                        inter_word = chr(first_parts.index(tmp_word[0])*588+second_parts.index(tmp_word[1]+tmp_word[2])*28+44032)
                elif len(tmp_word) == 4:
                        inter_word = chr(first_parts.index(tmp_word[0])*588+second_parts.index(tmp_word[1]+tmp_word[2])*28+third_parts.index(tmp_word[3])+44032)
            # print(tmp_word,inter_word)
                inter_line = inter_line + inter_word
                tmp_word = ""
                inter_word  = ""
                if divided_line[i] == "|":
                    inter_line = inter_line + " "
    # if len(tmp_word)  == 2 :
    #     inter_word = chr(first_parts.index(tmp_word[0])*588+second_parts.index(tmp_word[1])*28+44032)
    # elif len(tmp_word) == 3 :
    #     inter_word = chr(first_parts.index(tmp_word[0])*588+second_parts.index(tmp_word[1])*28+third_parts.index(tmp_word[2])+44032)
    # print(tmp_word,inter_word)
    inter_line = inter_line + ']\n'
    return inter_line

def write_string_to_file(temp_str, file_name):  
    #the encoding must be same with the str  
    file_object = open(file_name, 'w', encoding="utf-8")    
    file_object.write(temp_str)     
    file_object.close()  


# 读取所有韩文字单个字拼音——最后直接查找替换
kr_dic = {}
with open("kr_sound.csv","r") as csvfiler:
    read = csv.reader(csvfiler)
    for line in read:
        if not line:
            break
        kr_dic[line[0]] = line[1]

# 编译所有必须音变规则
necessary_re = []
replace_str = {}
necessary_re_compile(necessary_re,replace_str)
# print(len(necessary_re))
# print(necessary_re)
# pdb.set_trace()

data_files = glob.glob(os.getcwd() + "/lyrics/*.txt")  
print ("the result files save in the " + os.getcwd())  
for each_file in data_files:  
    print (each_file + "-"*5 + ">dealing")   #begin to deal file  
    with codecs.open(each_file, 'r', encoding="utf-8") as read_file:  
        temp_file_string = ""  
        for each_line in read_file:  
            if each_line.strip() == "":  
                continue
            temp_line = ""  
            # 一行一行进行处理，流程：
            # 1. 第一遍遍历，把所有韩文字拆分成辅音、元音、收音的形式，空格（即隔写处）采用|替换，每个字与字之间使用-连字符替换
            # print("source_line"+each_line)
            divided_line = divide_kr_line(each_line)
            # print("divided_line"+divided_line)
            # 2. 检查音变规则匹配是否匹配，匹配则进行替换
            temp_line = divided_line
            for x in range(0,len(necessary_re)):
                temp_line = re.sub(necessary_re[x], replace_str[necessary_re[x]], temp_line)
            # pdb.set_trace()
            # print("replaced_line"+temp_line)
            # 3. 第二遍遍历，把拆分的韩文字合并成一个整字
            kr_yinbiao = inter_kr_line(temp_line)
            # print("kr_yinbiao"+kr_yinbiao)
            # 4. 第三遍遍历，把每个韩文字查表换成拼音
            la_yinbiao = ""
            for i in range(0,len(kr_yinbiao)):
                if kr_yinbiao[i] in kr_dic.keys():
                    la_yinbiao = la_yinbiao + kr_dic[kr_yinbiao[i]] + '-'
                elif kr_yinbiao[i] == ' ' or kr_yinbiao[i] == ']':
                    if la_yinbiao[-1] == '-':
                        la_yinbiao = la_yinbiao[:-1] + kr_yinbiao[i]
                    else:
                        la_yinbiao = la_yinbiao + kr_yinbiao[i]
                else:
                    la_yinbiao = la_yinbiao + kr_yinbiao[i]
            # print("la_yinbiao"+la_yinbiao)
            # for i in range(0, len(each_line)):
            #     if each_line[i] >= u'\uAC00' and each_line[i] <= u'\uD7AF':  
            #         temp_line = temp_line + divide_korean(each_line[i]) + '-'
            #     elif each_line[i] ==' ':
            #         temp_line = temp_line[:-1] + '|'
            #     elif each_line[i] == "\n":
            #         break
            #     else :  
            #         temp_line = temp_line  + each_line[i]
            temp_line = each_line.strip('\n') +  '\n'  +   kr_yinbiao.strip('\n') +  '\n'  + la_yinbiao.strip('\n')
            # re.sub('ㄱ/ㄴ/ㄷ/ㄹ/ㅁ/ㅂ/ㅅ/ㅈ/ㅊ/ㅋ/ㅌ/ㅍ|ㅇ', '|ㄱ/ㄴ/ㄷ/ㄹ/ㅁ/ㅂ/ㅅ/ㅈ/ㅊ/ㅋ/ㅌ/', temp_line, count=0, flags=0)
            temp_file_string = temp_file_string + temp_line +  '\n' 
        temp_file_string = temp_file_string[:-1]
        print ( each_file + "-"*5 + ">finished")   #finish  
        #the name of new file to save the result, the new file is in the current dir  
        new_filename = "./new_divide/"+os.path.splitext(os.path.basename(each_file))[0] + ".txt"  
        #write to the file  
        write_string_to_file(temp_file_string, new_filename)  

# def double2single(double3):
#     if double3 == third_parts[2]:
#         return third_parts[1] + third_parts[1]
#     elif double3 == third_parts[3]:
#         return third_parts[1] + third_parts[19]
#     elif double3 == third_parts[5]:
#         return third_parts[4] + third_parts[22]
#     elif double3 == third_parts[6]:
#         return third_parts[4] + third_parts[27]
#     elif double3 == third_parts[9]:
#         return third_parts[8] + third_parts[1]
#     elif double3 == third_parts[10]:
#         return third_parts[8] + third_parts[16]
#     elif double3 == third_parts[11]:
#         return third_parts[8] + third_parts[17]
#     elif double3 == third_parts[12]:
#         return third_parts[8] + third_parts[19]
#     elif double3 == third_parts[13]:
#         return third_parts[8] + third_parts[25]
#     elif double3 == third_parts[14]:
#         return third_parts[8] + third_parts[26]
#     elif double3 == third_parts[15]:
#         return third_parts[8] + third_parts[27]
#     elif double3 == third_parts[18]:
#         return third_parts[17] + third_parts[19]
#     elif double3 == third_parts[20]:
#         return third_parts[19] + third_parts[19]
#     else:
#         print("input error, double3 must be in [ 'ㄲ', 'ㄳ',  'ㄵ', 'ㄶ',  'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅄ', 'ㅆ']")

# def third2first(double3):
#     if double3 == third_parts[1]:
#         return 0
#     elif double3 == third_parts[2]:
#         return 1
#     elif double3 == third_parts[4]:
#         return 2
#     elif double3 == third_parts[7]:
#         return 3
#     elif double3 == third_parts[8]:
#         return 5
#     elif double3 == third_parts[16]:
#         return 6
#     elif double3 == third_parts[17]:
#         return 7
#     elif double3 == third_parts[19]:
#         return 9
#     elif double3 == third_parts[20]:
#         return 10
#     elif double3 == third_parts[21]:
#         return 11
#     elif double3 == third_parts[22]:
#         return 12
#     elif double3 == third_parts[23]:
#         return 14
#     elif double3 == third_parts[24]:
#         return 15
#     elif double3 == third_parts[25]:
#         return 16
#     elif double3 == third_parts[26]:
#         return 17
#     elif double3 == third_parts[27]:
#         return 18

# 单收音连音化正则模式编译
# single3_junk = [1,4,7,8,16,17,19,22,23,24,25,26,27]
# double3_junk = [2,3,5,6,9,10,11,12,13,14,15,18,20]
# double2single_dir = {}
# for x in double3_junk:
#     double2single_dir[x] = double2single(third_parts[x])
#     # print(third_parts[x], double2single_dir[x])
# single3_junk_re = {}
# double3_junk_re = {}
# third2first_dic = {}
# for x in range(1,len(third_parts)):
#     # print(third_parts[x])
#     if third_parts[x] in first_parts:
#         third2first_dic[x] = third2first(third_parts[x])
#         # print(third2first_dic[x])
#         # print(third_parts[x],first_parts[third2first_dic[x]])



# temp_line = 'ㄱㅓㄱ-ㅈㅓㅇ-ㄷㅗ|ㅅㅡㄹ-ㅍㅡㅁ-ㄷㅗ|ㄷㅏ|ㄲㅡㅌ-ㄴㅏㄹ|ㅈㅜㄹ|ㅇㅏㄹ-ㅇㅏㅆ-ㅇㅓ'

# for x in single3_junk:
#     # print(third_parts[x])
#     single3_junk_re[x] = re.compile(third_parts[x]+'-'+'ㅇ')
#     # print(single3_junk_re[x])

# # 单收音正则匹配替换
# for x in single3_junk:
#     if x == 27:
#         temp_line = re.sub(single3_junk_re[x], '-'+'ㅇ', temp_line)
#     else:
#         temp_line = re.sub(single3_junk_re[x], '-'+first_parts[third2first_dic[x]], temp_line)
# print(temp_line)

# 双收音正则匹配替换
# for x in double3_junk:
#     double3_junk_re[x] = re.compile(third_parts[x]+'-'+'ㅇ')
#     print(double3_junk_re[x])
# for x in double3_junk:
#     doubledivide = double2single(third_parts[x])
#     if x in [2,5,9,10,11,13,14]:
#         temp_line = re.sub(double3_junk_re[x], doubledivide[0]+'-'+doubledivide[1], temp_line)
#     elif x in [3,12,18,20]:
#         temp_line = re.sub(double3_junk_re[x], doubledivide[0]+'-'+first_parts[10], temp_line)
#     elif x in [6.15]:
#         temp_line = re.sub(double3_junk_re[x], doubledivide[0]+'-'+'ㅇ', temp_line)
# print(temp_line)

# ㅎ的非标准连音
# ha_junk_re = {}
# ha_junk_re[4] = re.compile(third_parts[4]+'-'+'ㅎ')
# ha_junk_re[8] = re.compile(third_parts[8]+'-'+'ㅎ')
# ha_junk_re[16] = re.compile(third_parts[16]+'-'+'ㅎ')
# for key,value in ha_junk_re.items():
#     temp_line = re.sub(ha_junk_re[key], '-'+first_parts[third2first_dic[key]], temp_line)

# necessary_re = []
# replace_str = {}



# [必须规则]单收音连音化
# single_link_former= ["ㄱ","ㄴ","ㄷ","ㄹ","ㅁ","ㅂ","ㅅ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ"]
# single_link_later = ["ㅇ"]
# for x in single_link_former:
#     for y in single_link_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = '-'+x
# "ㄱ/ㄴ/ㄷ/ㄹ/ㅁ/ㅂ/ㅅ/ㅈ/ㅊ/ㅋ/ㅌ/ㅍ|ㅇ"->"|ㄱ/ㄴ/ㄷ/ㄹ/ㅁ/ㅂ/ㅅ/ㅈ/ㅊ/ㅋ/ㅌ/ㅍ"

# [必须规则]ㅎ的脱落现象
# ha_shedding_former = ["ㅎ"]
# ha_shedding_later = ["ㅇ"]
# for x in ha_shedding_former:
#     for y in ha_shedding_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = '-'+y
# "ㅎ|ㅇ"->"|ㅇ"

# [必须规则]双收音连音化
# double_link_former = ["ㄲ","ㄵ","ㄺ","ㄻ","ㄼ","ㄾ","ㄿ"]
# double_link_later = ["ㅇ"]
# for x in double_link_former:
#     for y in double_link_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         doubledivide = double2single(x)
#         replace_str[re.compile(x+'-'+y)] = doubledivide[0]+'-'+doubledivide[1]
# "ㄲ/ㄵ/ㄺ/ㄻ/ㄼ/ㄾ/ㄿ|ㅇ"->"ㄱㄱ/ㄴㅈ/ㄹㄱ/ㄹㅁ/ㄹㅂ/ㄹㅌ/ㄹㅍ|ㅇ"->"ㄱ/ㄴ/ㄹ/ㄹ/ㄹ/ㄹ/ㄹ|ㄱ/ㅈ/ㄱ/ㅁ/ㅂ/ㅌ/ㅍ"
# double_link_former = ["ㄶ","ㅀ"]
# for x in double_link_former:
#     for y in double_link_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         doubledivide = double2single(x)
#         replace_str[re.compile(x+'-'+y)] = doubledivide[0]+'-'+y
# "ㄶ/ㅀ|ㅇ"->"ㄴㅎ/ㄹㅎ|ㅇ"->"ㄴ/ㄹ|ㅇ"
# double_link_former = ["ㄳ","ㄽ","ㅄ","ㅆ"]
# for x in double_link_former:
#     for y in double_link_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         doubledivide = double2single(x)
#         replace_str[re.compile(x+'-'+y)] = doubledivide[0]+'-'+first_parts[10]
# "ㄳ/ㄽ/ㅆ/ㅄ|ㅇ"->"ㄱㅆ/ㄹㅆ/ㅅㅆ/ㅂㅆ|ㅇ"->"ㄱ/ㄹ/ㅅ/ㅂ|ㅆㅇ"

# # [可选规则]ㅎ的非标准连音
# ha_link_former= ["ㄴ","ㄹ","ㅁ"]
# ha_link_later = ["ㅎ"]
# for x in ha_link_former:
#     for y in ha_link_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = '-'+x
# # "ㄴ/ㄹ/ㅁ|ㅎ"->"|ㄴ/ㄹ/ㅁ"

# 连音选择：只要隔写就不发生音变，音变只在未隔写的词中发生；所以全部采用本音进行连，因为不可分割


# [必须规则]收音鼻音化
# nasal_former = ["ㄱ","ㅋ","ㄲ","ㄺ","ㄳ"]
# nasal_later = ["ㄴ","ㅁ"]
# for x in nasal_former:
#     for y in nasal_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = 'ㅇ'+'-'+y
# nasal_former = ["ㄷ","ㅌ","ㅅ","ㅈ","ㅊ","ㅆ","ㅎ"]
# for x in nasal_former:
#     for y in nasal_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = 'ㄴ'+'-'+y
# nasal_former = ["ㅂ","ㅍ","ㅄ","ㄿ"]
# for x in nasal_former:
#     for y in nasal_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = 'ㅁ'+'-'+y
# nasal_former_change = ["ㅇ","ㄴ","ㅁ"]
# "ㄱ/ㅋ/ㄲ/ㄺ/ㄳ|ㄴ/ㅁ"->"ㅇ|ㄴ/ㅁ"，"ㄷ/ㅌ/ㅅ/ㅈ/ㅊ/ㅆ/ㅎ|ㄴ/ㅁ"->"ㄴ|ㄴ/ㅁ"，"ㅂ/ㅍ/ㅄ/ㄿ|ㄴ/ㅁ"->"ㅁ|ㄴ/ㅁ"

# # [可选规则]辅音鼻音化（汉字词中）
# # first_nasal_re = {}
# nasal_former = ["ㅇ","ㅁ"]
# nasal_later = ["ㄹ"]
# for x in nasal_former:
#     for y in nasal_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = x+'-'+ 'ㄴ'
# # "ㅇ/ㅁ|ㄹ"->"ㅇ/ㅁ|ㄴ"

# # [可选规则]收辅音鼻音化（汉字词中）
# first_nasal_re = {}
# # nasal_former = ["ㄱ","ㅂ"]
# nasal_former = ["ㄱ"]
# nasal_later = ["ㄹ"]
# for x in nasal_former:
#     for y in nasal_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = 'ㅇ'+'-'+ 'ㄴ'
# nasal_former = ["ㅂ"]
# for x in nasal_former:
#     for y in nasal_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = 'ㅁ'+'-'+ 'ㄴ'
# # "ㄱ|ㄹ"->"ㅇ|ㄴ"，"ㅂ|ㄹ"->"ㅁ|ㄴ"


# [必须规则]阻塞音紧音化
# tight_former = ["ㄱ","ㅋ","ㄲ","ㄺ","ㄳ","ㄷ","ㅌ","ㅅ","ㅈ","ㅊ","ㅆ","ㅂ","ㅍ","ㅄ","ㄿ"]
# tight_later = ["ㄱ","ㄷ","ㅂ","ㅅ","ㅈ"]
# for x in tight_former:
#     for y in tight_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = x+'-'+ tight(y)
# "ㄱ/ㅋ/ㄲ/ㄺ/ㄳ/ㄷ/ㅌ/ㅅ/ㅈ/ㅊ/ㅆ/ㅂ/ㅍ/ㅄ/ㄿ|ㄱ/ㄷ/ㅂ/ㅅ/ㅈ"->"ㄱ/ㅋ/ㄲ/ㄺ/ㄳ/ㄷ/ㅌ/ㅅ/ㅈ/ㅊ/ㅆ/ㅂ/ㅍ/ㅄ/ㄿ|ㄲ/ㄸ/ㅃ/ㅆ/ㅉ"

# # [可选规则]词干ㄴㅁ
# tight_former = ["ㄴ","ㄵ","ㅁ","ㄻ"]
# tight_later = ["ㄱ","ㄷ","ㅅ","ㅈ"]
# for x in tight_former:
#     for y in tight_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = x+'-'+ tight(y)
# # "ㄴ/ㄵ/ㅁ/ㄻ|ㄱ/ㄷ/ㅅ/ㅈ"->"ㄴ/ㄵ/ㅁ/ㄻ|ㄲ/ㄸ/ㅆ/ㅉ"

# # [可选规则]汉字词ㄹ
# tight_former = ["ㄹ"]
# tight_later = ["ㄷ","ㅅ","ㅈ"]
# for x in tight_former:
#     for y in tight_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = x+'-'+ tight(y)
# # "ㄹ|ㄷ/ㅅ/ㅈ"->"ㄹ|/ㄸ/ㅆ/ㅉ"

# # [可选规则]合成词
# # [可选规则]ㄹ词尾
# tight_former = ["ㄹ"]
# tight_later = ["ㄱ","ㄷ","ㅂ","ㅅ","ㅈ"]
# for x in tight_former:
#     for y in tight_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = x+'-'+ tight(y)
# # "ㄹ/을|ㄱ/ㄷ/ㅂ/ㅅ/ㅈ"->"ㄹ/을|ㄲ/ㄸ/ㅃ/ㅆ/ㅉ"

# # [可选规则]ㄹ双收音
# tight_former = ["ㄼ","ㄾ"]
# tight_later = ["ㄱ","ㄷ","ㅅ","ㅈ"]
# for x in tight_former:
#     for y in tight_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = x+'-'+ tight(y)
# # "ㄼ/ㄾ|ㄱ/ㄷ/ㅅ/ㅈ"->"ㄼ/ㄾ|ㄲ/ㄸ/ㅆ/ㅉ"

# [必须规则]ㅎㅅ相遇
# tight_former = ["ㅎ","ㄶ","ㅀ"]
# tight_later = ["ㅅ"]
# for x in tight_former:
#     for y in tight_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = x+'-'+ tight(y)
# "ㅎ/ㄶ/ㅀ|ㅅ"->"ㅎ/ㄶ/ㅀ|ㅆ"


# # [可选规则]颚音化
# palatalization_former = ["ㄷ","ㅌ"]
# palatalization_later = ["ㅇㅣ"]
# for x in palatalization_former:
#     necessary_re.append(re.compile(x+'-'+y))
#     replace_str[re.compile(x+'-'+y)] = '-' + palatalize(x) + 'ㅣ'
# # "ㄷ/ㅌ|ㅇㅣ "->"|ㅈ/ㅊㅣ "

# [必须规则]ㅎ在前送气化
# aspiration_former = ["ㅎ","ㄶ","ㅀ"]
# aspiration_later = ["ㄱ","ㄷ","ㅈ"]
# for x in aspiration_former:
#     for y in aspiration_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = x+'-'+ aspirate(y)
# "ㅎ/ㄶ/ㅀ|ㄱ/ㄷ/ㅈ"->"ㅎ/ㄶ/ㅀ|ㅋ/ㅌ/ㅊ"

# [必须规则]ㅎ在后送气化——感觉貌似没什么用啊，就算送气化之后，发音还是感召非送气化来发啊
# aspiration_former2 = ["ㄱ","ㄲ","ㄺ","ㄳ","ㄷ","ㅅ","ㅈ","ㅊ","ㅌ","ㅂ","ㅄ","ㄿ"]
# aspiration_former = ["ㄱ","ㄲ","ㄺ","ㄳ"]
# aspiration_later = ["ㅎ"]
# for x in aspiration_former:
#     for y in aspiration_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = aspirate("ㄱ")+'-'+y
# aspiration_former = ["ㄷ","ㅅ","ㅈ","ㅊ","ㅆ","ㅎ"]
# for x in aspiration_former:
#     for y in aspiration_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = aspirate("ㄷ")+'-'+y
# aspiration_former= ["ㅂ","ㅄ","ㄿ"]
# for x in aspiration_former:
#     for y in aspiration_later:
#         necessary_re.append(re.compile(x+'-'+y))
#         replace_str[re.compile(x+'-'+y)] = aspirate("ㅂ")+'-'+y
# "ㄱ/ㄲ/ㄺ/ㄳ/ㄷ/ㅅ/ㅈ/ㅊ/ㅆ/ㅎ/ㅂ/ㅄ/ㄿ|ㅎ"->"ㅋ/ㅋ/ㅋ/ㅋ/ㅌ/ㅌ/ㅌ/ㅌ/ㅌ/ㅍ/ㅍ/ㅍ|ㅎ"
# # [可选规则]颚音化&送气化
# x = "ㄷ"
# y = "ㅎㅣ"
# necessary_re.append(re.compile(x+'-'+y))
# replace_str[re.compile(x+'-'+y)] = '-'+'ㅊ'+'ㅣ'
# # "ㄷ|ㅎㅣ "->"ㅌ|ㅎㅣ"->"|ㅊㅣ"
# for x in range(0,len(necessary_re)):
#     print(necessary_re[x])
# print(len(necessary_re))
# [必须规则]收音读音对应（单收音没有问题，主要是双收音有时候读左边，有时候读右边）
def present_3part_sound(single):
    if single in ["ㄴ","ㄵ","ㄶ"]:
        return "ㄴ"
    elif single in ["ㅁ","ㄻ"]:
        return "ㅁ"
    elif single == "ㅇ":
        return "ㅇ"
    elif single == ["ㄹ","ㄼ","ㄽ","ㄾ","ㅀ "]:
        return "ㄹ"
    elif single == ["ㄱ","ㅋ","ㄲ","ㄺ ","ㄳ"]:
        return "ㄱ"
    elif single ==["ㄷ","ㅌ","ㅅ","ㅈ","ㅊ","ㅆ","ㅎ"]:
        return "ㄷ"
    elif single ==["ㅂ","ㅍ","ㅄ","ㄿ"]:
        return "ㅂ"
    else:
        print("input error, shouyin must be in ['ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']")
# temp_line = 'ㄱㅓㄱ-ㅈㅓㅇ-ㄷㅗ|ㅅㅡㄹ-ㅍㅡㅁ-ㄷㅗ|ㄷㅏ|ㄲㅡㅌ-ㄴㅏㄹ|ㅈㅜㄹ|ㅇㅏㄹ-ㅇㅏㅆ-ㅇㅓ'

# for x in range(0,len(necessary_re)):
#     temp_line = re.sub(necessary_re[x], replace_str[necessary_re[x]], temp_line)
# print(temp_line)

# first_parts_yin = ("k/g", "gg", "n","t/d","dd","l","m","p/b","bb","s(x)","ss(xx)","","c(j)/j","jj","C(q)","K","T","P","h")
# second_parts_yin =("a", "ae", "ya", "yae", "eo", "e", "yeo", "ye", "o", "wa", "wae", "oe", "yo", "u", "wo", "we", "wi", "yu", "eu", "ui", "i")  
# third_parts_yin = ("", "g", "g", "g/d", "n", "n/d", "n/h", "d", "l", "g/l", "m/l", "l/b", "l/d", "l/d", "b/l", "l/h", "m", "b", "b/d", "d", "d", "ng", "d", "d", "g", "d", "b", "d")  
# def divide_korean(temp_string):  
#     temp_string_value = ord(temp_string)  
#     part_1 = (temp_string_value - 44032) // 588  
#     part_2 = (temp_string_value - 44032 - part_1 * 588) // 28  
#     part_3 = (temp_string_value - 44032 ) % 28  
#     # return first_parts[part_1] + second_parts[part_2] + third_parts[part_3]  
#     return first_parts_yin[part_1] + second_parts_yin[part_2] + third_parts_yin[part_3]  
# 双收音正则匹配替换
# for x in double3_junk:
#     double3_junk_re[x] = re.compile(third_parts[x]+'-'+'ㅇ')
#     print(double3_junk_re[x])
# for x in double3_junk:
#     doubledivide = double2single(third_parts[x])
#     if x in [2,5,9,10,11,13,14]:
#         temp_line = re.sub(double3_junk_re[x], doubledivide[0]+'-'+doubledivide[1], temp_line)
#     elif x in [3,12,18,20]:
#         temp_line = re.sub(double3_junk_re[x], doubledivide[0]+'-'+first_parts[10], temp_line)
#     elif x in [6.15]:
#         temp_line = re.sub(double3_junk_re[x], doubledivide[0]+'-'+'ㅇ', temp_line)
# print(temp_line)

# 重新组合成字
# single_word = ""

# sentence = "["
# for i in range(0, len(temp_line)) :  
#     if temp_line[i] != '-' and temp_line[i] !='|' and temp_line[i] != '\n':
#         single_word = single_word + temp_line[i]
#     elif temp_line[i] == '-'  or temp_line[i] =='|' or temp_line[i] == '\n':
#         # print(single_word)
#         if len(single_word)  == 2 :
#             intergal_word = chr(first_parts.index(single_word[0])*588+second_parts.index(single_word[1])*28+44032)
#         elif len(single_word) == 3 :
#             intergal_word = chr(first_parts.index(single_word[0])*588+second_parts.index(single_word[1])*28+third_parts.index(single_word[2])+44032)
#         print(single_word,intergal_word)
#         sentence = sentence + intergal_word
#         single_word = ""
#         intergal_word  = ""
#         if temp_line[i] == "|":
#             sentence = sentence + " "
# if len(single_word)  == 2 :
#     intergal_word = chr(first_parts.index(single_word[0])*588+second_parts.index(single_word[1])*28+44032)
# elif len(single_word) == 3 :
#     intergal_word = chr(first_parts.index(single_word[0])*588+second_parts.index(single_word[1])*28+third_parts.index(single_word[2])+44032)
# print(single_word,intergal_word)
# sentence = sentence + intergal_word + ']\n'

# print(sentence)

# each_line = sentence
# tmp = ""
# for i in range(0, len(each_line)):  
#     if each_line[i] >= u'\uAC00' and each_line[i] <= u'\uD7AF':  
#         tmp = tmp + divide_korean(each_line[i]) + '-'
#     elif each_line[i] == "\n":
#         tmp = tmp[:-1]
#         continue
#     else :  
#         # continue
#         tmp = tmp + each_line[i]
# tmp = each_line.strip('\n') +  '\n'  +   tmp
# print(tmp)

# re.compile(pattern,flags=0)

# 编译一个正则表达式模式，返回一个模式对象

# 复制代码
# >>> import re
# >>> re1 = re.compile(r'hello')   #编译一个正则匹配模式
# >>> print(type(re1))
# <class '_sre.SRE_Pattern'>  #该模式是一个pattern对象
# >>> print(re.match(re1,'hello world').group())
# hello