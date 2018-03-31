# import codecs  
# import glob  
# import codecs  
# import os
import csv

# vowels and consonants
first_parts = ("ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ")  
first_parts_yin = ("k/g", "gg", "n","t/d","dd","l","m","p/b","bb","s(x)","ss(xx)","","c(j)/j","jj","C(q)","K","T","P","h")
second_parts =("ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅗㅏ", "ㅗㅐ", "ㅗㅣ", "ㅛ", "ㅜ", "ㅜㅓ", "ㅜㅔ", "ㅜㅣ", "ㅠ", "ㅡ", "ㅡㅣ", "ㅣ")  
second_parts_yin =("a", "ae", "ya", "yae", "eo", "e", "yeo", "ye", "o", "wa", "wae", "oe", "yo", "u", "wo", "we", "wi", "yu", "eu", "ui", "i")  
third_parts = ("", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ")  
third_parts_yin = ("", "g", "g", "g", "n", "n", "n", "d", "l", "g", "m", "l", "l", "l", "b", "l", "m", "b", "b/d", "d", "d", "ng", "d", "d", "g", "d", "b", "d")  

def print_all_kr(dic):
    for first in range(0,len(first_parts)):
        for second in range(0,len(second_parts)):
            for third in range(0,len(third_parts)):
                Sum = third + second*28 + first*588+44032
                kr_word = chr(Sum)
                if first in [9,10,12,14]:
                    if second in [0,1,4,5,8,9,10,11,13,14,15,18]:
                        if first == 9:
                            first_yin = 's'
                        elif first ==10:
                            first_yin ='ss'
                        elif first ==12:
                            first_yin = 'c/j'
                        else:
                            first_yin = 'C'
                    else:
                        if first == 9:
                            first_yin = 'x'
                        elif first ==10:
                            first_yin ='xx'
                        elif first ==12:
                            first_yin = 'j'
                        else:
                            first_yin = 'q'
                else:
                    first_yin = first_parts_yin[first]
                dic[kr_word] = first_yin + second_parts_yin[second] + third_parts_yin[third]
kr_word_dic = {}
print_all_kr(kr_word_dic)

with open("kr_sound.csv","w") as csvfiler:
    fw = csv.writer(csvfiler)
    for key,value in kr_word_dic.items():
        fw.writerow([key,value])
