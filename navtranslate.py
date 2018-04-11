import os
import sys
import urllib.request


# 번역 결과 언어 코드. 
# 1.ko : 한국어
# 2.en : 영어
# 3.zh-CN : 중국어 간체
# 4.zh-TW : 중국어 번체
# 5.es : 스페인어
# 6.fr : 프랑스어
# 7.vi : 베트남어
# 8.th : 태국어
# 9.id : 인도네시아어

# ko<->en, ko<->zh-CN, ko<->zh-TW, ko<->es, ko<->fr, ko<->vi, ko<->th, ko<->id, en<->ja, en<->fr 조합만 가능


client_id = sys.argv[1]
client_secret =  sys.argv[2]

encText = urllib.parse.quote("화려한 저 조명 아래에 서면\n걱정도 슬픔도 다 끝날 줄 알았어\n한걸음 두 걸음 올라갈수록")
data = "source=ko&target=zh-CN&text=" + encText
url = "https://openapi.naver.com/v1/language/translate"
# url = "https://openapi.naver.com/v1/krdict/romanization"
# url = "https://openapi.naver.com/v1/papago/n2mt"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
# request.add_header("Host"," openapi.naver.com")
# request.add_header("User-Agent"," Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0")
# try:
#     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
# except Exception as e:
#     print(zlib.decompress(e.read(),30))
response = urllib.request.urlopen(request, data=data.encode("utf-8"))
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)