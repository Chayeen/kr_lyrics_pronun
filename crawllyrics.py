# 爬取网易云音乐某个歌单里面所有歌曲的歌词
import json
import requests
import re
import urllib
from bs4 import *
import pdb
import sys
import os

# 955274121 韩语
# 614151599 Jachin喜欢的音乐
# 40131331 百变女王T-ara 绝妙中速慢节奏
# 53656860 T-ara无重复精选
# 153369263 Queen's福利，T-ara无重复最全收录

# 接收输入参数，必须是歌单的一串数字，默认爬取无重复精选；不是一串数字or唱过接收输入参数个数直接退出程序
if len(sys.argv) == 1:
    songlistid = "53656860"
elif len(sys.argv) == 2:
    try:
        songlistid = int(sys.argv[1])
    except Exception as e:
        print("input error! songlistid need a string of numbers, no more other character!")
        sys.exit(1)
    songlistid = sys.argv[1]
else:
    print("input params over 2, just input one songlistid!")
    sys.exit(1)

# 获取当前文件目录，检查是否有lyrics文件夹，如果不存在则自动新建文件夹
# pdb.set_trace()
File_Path = os.getcwd() +'/lyrics/'
if not os.path.exists(File_Path):
    os.makedirs(File_Path)

# 拼接请求数据包：只传url不能获得响应，需要传header
url = "http://music.163.com/playlist?id="+songlistid
headers = {"Host":" music.163.com","User-Agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0"}
request = urllib.request.Request(url,headers=headers)
# 发起请求
response = urllib.request.urlopen(request)
# 获取返回的网页，用utf-8编码解码：不decode的话text是十六进制，不是中文
html = response.read().decode('utf-8','ignore')
soup = BeautifulSoup(html, "html.parser")

for item in soup.ul.children:
    # 取出歌单里歌曲的id  形式为：/song?id=11111111
    song_id = item('a')[0].get("href",None)
    # 利用正则表达式提取出song_id的数字部分sid
    pat = re.compile(r'[0-9].*$')
    sid = re.findall(pat,song_id)[0]

    # 拼接url，获取真实的歌词页面，发起请求
    url = "http://music.163.com/api/song/lyric?"+"id="+str(sid)+"&lv=1&kv=1&tv=-1"
    html = requests.post(url)
    json_obj = html.text

    # 歌词是一个json对象，解析获取歌词文本
    j = json.loads(json_obj)
    try:
        lyric = j['lrc']['lyric']
    except KeyError:
        lyric = "无歌词"
    pat = re.compile(r'\[.*\]')
    lrc = re.sub(pat,"",lyric)
    lrc = lrc.strip()

    # 取出歌单里歌曲名，以歌曲名为文件名，新建文件存储歌词
    song_name = item('a')[0].get_text()
    # song_name.replace('/','_')
    # 上一句替换失败，只能暂时采取折中手段，如果歌曲名称中包含/字符就跳过无法保存，因为linux下文件命名规则不能包含/字符
    if "/" in song_name:
        continue
        # print(song_name)
        # pdb.set_trace()
    f=open('./lyrics/'+song_name+'.txt','w',encoding='utf-8')
    f.write(lrc)
    f.close()


# 代码参考：
# 作者：小太阳花儿
# 链接：https://www.jianshu.com/p/c0ae445023a2