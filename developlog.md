# 2018-03-22 22:09:54 最初的考虑
把韩语解析的python代码写出来（先实现一个基础版本，基于养乐多的基础发音教程，实现最基本的韩文字发音转换；后面再根据各种音变规则写一个存在音变的版本；如果能够识别韩语音乐发音，根据idol发音进行具体调整就更好了）：参考[python实现韩文分解](http://blog.csdn.net/u011289327/article/details/44618931)、[python爬取网易云音乐我的歌单歌词](https://www.jianshu.com/p/c0ae445023a2?from=timeline)[python爬歌词](https://www.cnblogs.com/Beyond-Ricky/p/6757954.html)、[韩语语音识别现状](http://www.wanjishu.com/p/qy073T170802.html)在语言学中，韩语属于黏着语，其自然词汇由大量词素聚集构成，同时语言具有丰富的音韵变化。黏着语是语言形态学中的一个语言类别，这一类别的语言需要大量依靠词素的屈折变化来表现文法关系。第一个主要是语言模型方面，韩语的自然语言单元是由空格分割开的字和词，长度不固定，有可能是实体词加助词，也可能是单独的实体词，对应于英语中的几个单词。第二个挑战是声学模型建模，黏着特性导致严重的协同发音，从而使声学模型的混淆度大大提升。解决方案，可以通过引入同位音素的概念来削弱声学模型的混淆程度，但实验证明这一方法尽管在单音子（monophone）声学模型建模单元上效果较为显著，但在常规语音识别系统所使用的三音子（triphone）声学模型建模单元上效果并不理想。如果按照书写方式来分，在韩语中共有首辅音19 种，元音21种，尾辅音27种。由于韵尾可以省略，因此韵尾共有28 种形式，由此可以推算出谚文数量为19×21×28=__11172__个。就发音而言，每种首辅音和元音都有其独特的发音，但是首辅音o为不发声辅音，而27 种韵尾则被归结为7组，每组中所有的尾辅音都与一个特定的首辅音发音相同。同时考虑到不含韵尾的情况，朝鲜语音节数量共计19×21×8=__3192__。韩语词汇在句中以空格分隔，其由若干谚文构成，谚文数量可以是一个或者多个。可以根据谚文字形简便获得其unicode编码。可以通过韩文的unicode编码反推罗马读音，加上一些韩文的变音规则，在资源极度缺乏的时候，可以用来自动生成韩语的声学训练语料，从unicode编码反推罗马读音的代码。base = 44032、df = int(integers[iElement]) - base、iONS = int(math.floor(df / 588)) + 1、iNUC = int(math.floor((df % 588) / 28)) + 1、iCOD = int((df % 588) % 28) + 1。鉴于这种统一的发音方式，先前的研究者通常将相同的发音首辅音和尾音归为同一音素，此种方法韩语音素集按照理论发音构建，包含18个首辅音、21个元音和1个尾辅音，共计40个音素。大多数时候，韩语的训练语料非常有限，又由于韩语是音形字，所以有很多学者研究从韩语形态学分析发音，自动生成训练的语音。[网易云音乐 歌词制作软件 BesLyric](http://www.cnblogs.com/BensonLaur/p/6262565.html)这个好厉害。——重新整理一下需求：想要一个批量韩语歌词发音生成的代码；首先批量的韩语歌词，通过爬取网易云音乐的歌词，每个歌词保存一个歌词文件；然后读取歌词文件中的韩文，批量输出发音（这里有几个问题，基础发音中，k/g b/p t/d s/x c/j c/q各种多音，主要是前三个不好判断；其次，如果存在音变现象，简单的音变还可以，比如说一些连音化，复杂一点的什么鼻音化、紧音化就不是很了解了；最后，有些处理是看心情的，不管怎么处理都可以，这时候就要与原音进行对比，找到最相似的音频了）；如果要和原音做对比再进行输出的话，首先就要对原音进行人声分离，还要对韩文字的几种发音处理情况进行发音，然后与分离出来的人声作对比，找到最相似的那一组发音，感觉就是在做语音识别的活（如果能够自动生成歌词就更好了，通过播放音乐，识别音乐中的人声歌词，并且根据时间，自动制作歌词时间轴）

# 2018-03-22 22:11:00
今天晚上先把 python 爬取网易云歌单歌词的代码搞定，参考
[python爬取网易云音乐我的歌单歌词](https://www.jianshu.com/p/c0ae445023a2?from=timeline)
[python爬歌词](https://www.cnblogs.com/Beyond-Ricky/p/6757954.html)

# 2018-03-22 22:45:42
1. 刚刚修改缩进，本来准备直接运行，又弄了下github在chayeen这台服务器上的账号，直接把之前本地建立的私钥copy过去不能用，原因是权限太高，按照网上说的降低权限到0600就可以用了`chmod 0600 /root/.ssh/id_rsa`命令。——现在应该就可以直接从服务器提交到远程github上了，密钥使用还是有密码，照常。
2. 然后修改了下代码的url，改成自己的歌单试试看：http://music.163.com/#/playlist?id=614151599
- 遇到没有requests库的问题，直接pip3 install 安装一下就可以了。

> [root@iz2ze8e1dj06n0wjqj19n2z kr_lyrics_pronun]# python3 crawllyrics.py 
> Traceback (most recent call last):
>   File "crawllyrics.py", line 3, in <module>
>     import requests
> ImportError: No module named 'requests'
> [root@iz2ze8e1dj06n0wjqj19n2z kr_lyrics_pronun]# pip3 install requests

- 又遇到没有 bs4 的问题照样安装就可以了

> [root@iz2ze8e1dj06n0wjqj19n2z kr_lyrics_pronun]# python3 crawllyrics.py 
> Traceback (most recent call last):
>   File "crawllyrics.py", line 6, in <module>
>     from bs4 import *
> ImportError: No module named 'bs4'
> [root@iz2ze8e1dj06n0wjqj19n2z kr_lyrics_pronun]# pip3 install beautifulsoup4
    
- 莫名其妙的错误：

> [root@iz2ze8e1dj06n0wjqj19n2z kr_lyrics_pronun]# python3 crawllyrics.py 
> /usr/lib/python3.4/site-packages/bs4/__init__.py:181: UserWarning: No parser was explicitly specified, so I'm using the best available HTML parser for this system ("html.parser"). This usually isn't a problem, but if you run this code on another system, or in a different virtual environment, it may use a different parser and behave differently.
> 
> The code that caused this warning is on line 24 of the file crawllyrics.py. To get rid of this warning, change code that looks like this:
> 
>  BeautifulSoup(YOUR_MARKUP})
> 
> to this:
> 
>  BeautifulSoup(YOUR_MARKUP, "html.parser")
> 
>   markup_type=markup_type))
> Traceback (most recent call last):
>   File "crawllyrics.py", line 30, in <module>
>     song_id = item('a')[0].get("href",None)
> TypeError: 'NavigableString' object is not callable

- 改了下第24行，再试试：

> [root@iz2ze8e1dj06n0wjqj19n2z kr_lyrics_pronun]# python3 crawllyrics.py 
> Traceback (most recent call last):
>   File "crawllyrics.py", line 30, in <module>
>     song_id = item('a')[0].get("href",None)
> TypeError: 'NavigableString' object is not callable

- 没有之前的提示了，但是还是有error
2018-03-22 23:21:57，卡住了，这个应该是bs4这个python包不太会用的缘故，而且感觉他的解析也有点问题，估计网易云对网页进行了一些修改，考虑考虑重新弄一下，有点难度。

# 2018-03-26 22:39:25
晚上重新各种搜了下,发现是最开始使用的url不对,在网易云音乐中所有的链接都要把 '#' 删掉才行，否则获取的URL是假链接。改了之后就可以l了。
刚刚简单修改了下，让所有的歌词文件分歌曲题目放在了lyrics文件夹中。刚刚遇到了一个bug在标题中有空格&其他特殊字符，"我有一个道姑朋友（……）"这首歌就没有正常存入，不过考虑到本来就是弄韩语的，所以直接把这个bug忽视掉了，存了3个歌单的韩语歌，随便打开了个看了下，还是不错，格式可能需要微调，不调也行。可以进行下一步了

# 2018-03-26 22:50:11
下一个功能就是，把韩语文字标上发音。
参考[python实现韩文分解](http://blog.csdn.net/u011289327/article/details/44618931)

直接copy了个代码，出了点问题：
UnicodeError: UTF-16 stream does not start with BOM

2018-03-26 23:47:18，问题解决了，因为原始文件是utf-8格式的，而代码里是utf-16格式的，全部改成utf-8就好了。
现在已经能够直接输出所有拼音了，不过不包含音变情况。争取明天能够添加上连音的情况。而且现在收音部分的发音还有点点问题，主要是双收音的发音问题，以及结合后面的音变问题。

