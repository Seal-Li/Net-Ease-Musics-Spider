# -*- coding:'utf-8' -*-
import re
import time
import json
import requests
from bs4 import BeautifulSoup

url = 'https://music.163.com/discover/toplist?id=3778678'
headers = """{
    "Cookie":"JSESSIONID-WYYY=kO%2BqRMsTprWcwq1s79qUT0lik2J5S33RAcuTz2B3c7vK87XeK21B%2Bz%2BriYoOj9ikAs9krGdjbkrtSoB9mcmw4UmQSNVZqlEfvMa8QfB7iXY2YDJ8F5RWAqXOzF9AuoKPkWdjHePhzqvbTxD8x%5CbfCA2ZUP%2Bu%5CjBVM7vW33jD511A3Tph%3A1541753312389; _iuqxldmzr_=32; _ntes_nnid=fdf5704172bbe9ddecf557c0a6af5cf9,1540386322920; _ntes_nuid=fdf5704172bbe9ddecf557c0a6af5cf9; __utma=94650624.1212762038.1540386324.1541741613.1541751514.22; __utmz=94650624.1541741613.21.12.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; WM_NI=omUzOdaMdIpjUv7nR8kR6cCSowoFrkFMyWWgUJdfFgMQEUub1mtoMIAuMj%2BKHKqLJ7WrGVV%2BJWojcgZFn2HUI32NnqhZMMEUkj%2BFBYPeRTITpJbjsBJNF2pFcSA3i2BpN2w%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed0d57aafad8cd6ef4d87eb8ab7c54b929a8fbbf245a7b0f8cce96ebca9ff98eb2af0fea7c3b92aadb39b9bce70a393acaaf36297aaf98fd134a98efa84c259ada9a1a7f1618693b7b8d66d9796ac87c56d8f8f8bb6f86af3b3bc90d04383ab838baa418c95bfadc93d95ae89b7d5218a89a18be26d9a9aa2d3cb5f8bedfeafed7bac8683aec85fa9b6e5a7c15394bb9eb5cc60b496ae8bf24a8a928ad3f34ea18d8fd4ec3a82b082d3f637e2a3; WM_TID=tj0jYAU1wWNEFBVVUEZ9bZgtXONn8Wxm; __utmb=94650624.4.10.1541751514; __utmc=94650624",
    "Host":"music.163.com",
    "Referer":"https://music.163.com/",
    "User-Agent":"Mozilla/5.0"
    }"""
      #设置请求头，重点在于设置Cookie
post_headers = json.loads(headers)

def get_soup(url):
      #获取网易云某排行榜歌单页面信息并解析
    global post_headers
    try:
        r = requests.get(url,headers = post_headers)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        html = r.text
        soup = str(BeautifulSoup(html,'lxml'))
        # print(soup)
    except:
        print('访问失败')

    return soup

def get_information(soup):
      #获取歌曲名和歌曲id
    expr = r'<ul class="f-hide">.*</ul>'
      #匹配包含歌名和id字段
    song_id_expr = r'<li><a href="/song\?id=(\d*?)">.*?</a></li>'
    song_name_expr = r'<li><a href="/song\?id=\d*?">(.*?)</a></li>'
    
    all_information = re.compile(expr).findall(soup)
    # print(all_information)
    hot_information = all_information[0]
    # print(hot_information)
    song_id = re.compile(song_id_expr).findall(hot_information)
    song_name = re.compile(song_name_expr).findall(hot_information)
      #得到歌曲id和歌名的列表
    return song_id,song_name

def get_lyric(song_id,song_name):
	  #将歌词写入txt文件
    global post_headers
    lyric_url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(song_id) + '&lv=1&kv=1&tv=-1'
      #歌词url
    lyric_page = requests.post(lyric_url,headers = post_headers)
    html = str(lyric_page.text)
    if html:
        lyric_source = json.loads(html)
        if 'lrc'in lyric_source:
            lyric = lyric_source['lrc']['lyric']
            lyric = lyric_source['lrc']['lyric']
            regex = re.compile(r'\[.*\]')
            with open('hot_music_lyric.txt','a+',encoding = 'utf-8') as l:
                l.write(song_name + '\n' + lyric +'\n' + '=='*50 + '\n')
                l.close()
    print(song_name + '>>>歌词写入完成')

    return None

def get_comment(song_id,song_name):
	  #将评论写入txt文件
    global post_headers
    comment_url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' +str(song_id)+ '?csrf_token='
    data = {
        'params': 'AoF/ZXuccqvtaCMCPHecFGVPfrbtDj4JFPJsaZ3tYn9J+r0NcnKPhZdVECDz/jM+1CpA+ByvAO2J9d44B/MG97WhjmxWkfo4Tm++AfyBgK11NnSbKsuQ5bxJR6yE0MyFhU8sPq7wb9DiUPFKs2ulw0GxwU/il1NS/eLrq+bbYikK/cyne90S/yGs6ldxpbcNd1yQTuOL176aBZXTJEcGkfbxY+mLKCwScAcCK1s3STo=',
        'encSecKey': '365b4c31a9c7e2ddc002e9c42942281d7e450e5048b57992146633181efe83c1e26acbc8d84b988d746370d788b6ae087547bace402565cca3ad59ccccf7566b07d364aa1d5b2bbe8ccf2bc33e0f03182206e29c66ae4ad6c18cb032d23f1793420ceda05e796401f170dbdb825c20356d27f07870598b2798f8d344807ad6f2'
    }
      #参数data不能缺省
    comment_page = requests.post(comment_url,headers = post_headers,data = data)
    html = str(comment_page.text)
    if html:
        comments = []
        message = {}
        html = json.loads(html)
        for comment in html['hotComments']:  #获取热评信息
            message['nickname'] = comment['user']['nickname']
            message['content'] = comment['content']
            comments.append(message)
            message = {}
    
        with open('hot_music_comment.txt','a+',encoding = 'UTF-8') as c:
            c.write(song_name + ':' + '\n')
            for item in comments:
                c.write(str(item.keys()) + '\n' +str(item.values()))
            c.write('\n' + '=='*50 + '\n')
            c.close()
    print( song_name + '>>>热评写入完成'+ '\n' + '等待下一首..........'+ '\n')
    return None

def get_file(url):
    soup = get_soup(url)
    print(soup)
    song_id,song_name = get_information(soup)
    time1 = time.time()
    for s_id,s_name in zip(song_id,song_name):
        get_lyric(s_id,s_name)
        get_comment(s_id,s_name)
    time2 = time.time()
      #统计写入文本所需的总时间
    deta_time = time2 - time1
    print("文本写入共用时{}秒".format(deta_time))
    return None


def main(url):
    print("Begin get information,please wait for a while......")
    get_file(url)
    print("All information get finished !")
    return None

main(url)