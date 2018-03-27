#爬取网易云音乐我的歌单里面所有歌曲的歌词
import json
import requests
import re
import urllib
from bs4 import *
import pdb
# 955274121 韩语
# 614151599 我喜欢的
# 40131331 百变女王T-ara 绝妙中速慢节奏
# 53656860 T-ara无重复精选
# 153369263 Queen's福利，T-ara无重复最全收录
url = "http://music.163.com/playlist?id=153369263"
headers = {"Host":" music.163.com","User-Agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0"
#不必要的header属性可能会影响响应报文的编码方式，所以把它们注释掉
#"Accept":" text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#"Accept-Language":" zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
#"Referer":"http://music.163.com/",
#"Cookie": "JSESSIONID-WYYY=k52%2FPjMyNbX0v38jH2efUXwEIZpw2NagEUzwTX%2FgifMsoMswU6yo3NN%5C%2Bb9jCpsRFZIc6lvPUK9wEjgBzwM%2B1T%2FRyvRGHhqyWbdvEcugCbNqTihfxHK1el66fk%2BNntcSwGVOBMEwlcFDBusingcH76NIeAQwbC6h%5CcipxCdO8T5IfBVO%3A1510825875526; _iuqxldmzr_=32; _ntes_nnid=e5ec3ba6b841b9d3eadcb910066f4dcb,1510815153893; _ntes_nuid=e5ec3ba6b841b9d3eadcb910066f4dcb; __utma=94650624.1386008069.1510815154.1510815154.1510824076.2; __utmz=94650624.1510815154.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmb=94650624.2.10.1510824076; __utmc=94650624",
#"Connection": "keep-alive",
#"Upgrade-Insecure-Requests": "1"
}
#只传url不能获得响应，需要传header
request = urllib.request.Request(url,headers=headers)
response = urllib.request.urlopen(request)

#不decode的话text是十六进制，不是中文
html = response.read().decode('utf-8','ignore')
soup = BeautifulSoup(html, "html.parser")

# links = soup.find('ul', class_='f-hide').findall('a')
# song_id = link.get('href').split('=')[-1]
# song_name = link.get_text()
# print(song_id,song_name)

# print(soup)

# print(soup.ul.children)
#打开1.txt 把歌单中的歌词写入
# f=open('./myfavoritesong.txt','w',encoding='utf-8')
for item in soup.ul.children:
    #取出歌单里歌曲吗名
    song_name = item('a')[0].get_text()
    # print(song_name)
    # pdb.set_trace()
    f=open('./lyrics/'+song_name+'.txt','w',encoding='utf-8')
    # f.write(song_name)
    #取出歌单里歌曲的id  形式为：/song?id=11111111
    song_id = item('a')[0].get("href",None)
    #利用正则表达式提取出song_id的数字部分sid
    pat = re.compile(r'[0-9].*$')
    sid = re.findall(pat,song_id)[0]
    #这里的url是真实的歌词页面
    url = "http://music.163.com/api/song/lyric?"+"id="+str(sid)+"&lv=1&kv=1&tv=-1"
    html = requests.post(url)
    json_obj = html.text
    #歌词是一个json对象 解析它
    j = json.loads(json_obj)
    try:
        lyric = j['lrc']['lyric']
    except KeyError:
        lyric = "无歌词"
    pat = re.compile(r'\[.*\]')
    lrc = re.sub(pat,"",lyric)
    lrc = lrc.strip()
    # print(lrc)
    f.write(lrc)
    f.close()

# 作者：小太阳花儿
# 链接：https://www.jianshu.com/p/c0ae445023a2
# 來源：简书
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。