# kr_lyrics_pronun
First, crawl Korean songs lyrics from Netease cloud music and save them into single .txt file.

Then, add pronunciation for Korean lyrics based on Teacher Yang Leduo's course and save them into new .txt files.

Finally, the output files need to be checked with individual songs.

# functions to be implemented
1. crawl all song lyrics in a certain song list from Netease cloud music.——2018-03-26 22:43:17，crawllyrics.py accomplishes this function, but the song list id is confirmed. It should provide an interface to input the song list id. Optimize this after basic functions over.
2. save each song lyric into a txt file according a certain format.——2018-03-26 22:46:54, each song has a .txt file to save its lyrics. All lyrics are in folder lyrics/.
3. code the rules from Teacher Yang Leduo's course, including pronunciation courses and sound-changing courses.——2018-04-11 17:57:03，基本规则和音变规则编写OK
4. add pronunciation for each korean song lyric files into a new file.——2018-04-11 17:57:35，也能每个歌词存储到一个文件中
5. check with individual song for final examination.——当前还是采用人工判断的方式，现在主要只需要判断一些ㅎ的不规则连音、隔写两端的连音以及k/g,b/p,d/t之间的区分，现在还是人工重复听歌，相当于限制于本人的水平，可能有错误的地方。

# new functions
1. 对一首歌词进行分析，或者说给一段韩语文本，提取出其中的单词及语法知识：暂定的实现机制是，根据隔写对韩语文本进行切割，然后从NAVER中进行一对一查词输出结果保存；根据一行一行对文本进行查NAVER翻译输出结果保存
2. 想要对一首歌的音频进行处理，能够输入一段音频，输出一段文字，其实相当于就是语音识别了：即输入一首歌的mp3文件，输出一个txt文本，而且能够根据非人声歌词间隔，如果能够与标准的声音计算相似性，可以慢慢构造标注的数据集，或者说之前已经人工校验过的那些就是标注的数据集了——其实也不用这么夸张，能够对k/g,b/p,d/t进行识别区分就不错了；或者在有歌词的情况下，弄一个自动把歌词对应，输出歌词滚动时间的程序，以后也就不用人工打标时间了。

# deadline
180429——2018-04-11 18:00:14，之前说的基本功能都已经完成了，现在想要增加一些功能；争取能够实现新的功能1好了。
