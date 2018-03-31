#coding:utf-8  
  
import codecs  
import glob  
import codecs  
import os  

# vowels and consonants
first_parts = ("ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ")  
first_parts_yin = ("k/g", "gg", "n","t/d","dd","l","m","p/b","bb","s(x)","ss(xx)","","c(j)/j","jj","C(q)","K","T","P","h")
second_parts =("ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅗㅏ", "ㅗㅐ", "ㅗㅣ", "ㅛ", "ㅜ", "ㅜㅓ", "ㅜㅔ", "ㅜㅣ", "ㅠ", "ㅡ", "ㅡㅣ", "ㅣ")  
second_parts_yin =("a", "ae", "ya", "yae", "eo", "e", "yeo", "ye", "o", "wa", "wae", "oe", "yo", "u", "wo", "we", "wi", "yu", "eu", "ui", "i")  
third_parts = ("", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ")  
third_parts_yin = ("", "g", "g", "g/d", "n", "n/d", "n/h", "d", "l", "g/l", "m/l", "l/b", "l/d", "l/d", "b/l", "l/h", "m", "b", "b/d", "d", "d", "ng", "d", "d", "g", "d", "b", "d")  
def divide_korean(temp_string):  
    temp_string_value = ord(temp_string)  
    part_1 = (temp_string_value - 44032) // 588  
    part_2 = (temp_string_value - 44032 - part_1 * 588) // 28  
    part_3 = (temp_string_value - 44032 ) % 28  
    # return first_parts[part_1] + second_parts[part_2] + third_parts[part_3]  
    return first_parts_yin[part_1] + second_parts_yin[part_2] + third_parts_yin[part_3]  


def label_korean(temp_string):  
    temp_string_value = ord(temp_string)  
    part_1 = (temp_string_value - 44032) // 588  
    part_2 = (temp_string_value - 44032 - part_1 * 588) // 28  
    part_3 = (temp_string_value - 44032 ) % 28  
    return first_parts[part_1] + second_parts[part_2] + third_parts[part_3]  

# old_korean_dictionary = {}  
# read_file = codecs.open("old_korean_dictionary.txt", 'r', encoding="utf-8")  
# for each_line in read_file:  
#     old_korean, dividing_parts = each_line.split()  
#     old_korean_dictionary[old_korean] = dividing_parts  

# wriet string to txt file  
def write_string_to_file(temp_str, file_name):  
    #the encoding must be same with the str  
    file_object = open(file_name, 'w', encoding="utf-8")    
    file_object.write(temp_str)     
    file_object.close()  
  
  
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
            for i in range(0, len(each_line)):  
                # if each_line[i] in old_korean_dictionary:  
                #     temp_line = temp_line + old_korean_dictionary.get(each_line[i])  
                # elif each_line[i] >= u'\uAC00' and each_line[i] <= u'\uD7AF':  
                if each_line[i] >= u'\uAC00' and each_line[i] <= u'\uD7AF':  
                    temp_line = temp_line + divide_korean(each_line[i]) + '-'
                elif each_line[i] == "\n":
                    temp_line = temp_line[:-1]
                    continue
                else :  
                    # continue
                    temp_line = temp_line[:-1]  + each_line[i]
                    # temp_line = temp_line  + each_line[i]
            # temp_line = temp_line[:-1]
            temp_line = each_line.strip('\n') +  '\n'  +   temp_line    
            temp_file_string = temp_file_string + temp_line +  '\n' 
        temp_file_string = temp_file_string[:-2]
        print ( each_file + "-"*5 + ">finished")   #finish  
        #the name of new file to save the result, the new file is in the current dir  
        new_filename = "./divide/"+os.path.splitext(os.path.basename(each_file))[0] + ".txt"  
        #write to the file  
        write_string_to_file(temp_file_string, new_filename)  



# 代码参考：https://blog.csdn.net/u011289327/article/details/44618931