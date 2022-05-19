import requests
def GetMusic(song_id,song_name):
    headers = {'user-agent':'Mozilla/5.0'}
    url = 'http://music.163.com/song/media/outer/url?id=' + str(song_id) + '.mp3'
    try:
        r = requests.get(url,headers = headers)
        r.raise_for_status
        with open(song_name + '.mp3','wb') as m:
            m.write(r.content)
            m.close()
            print(song_name + '>>>下载完成')
    except:
        print(song_name + '>>>下载失败')
        pass
    return None

def main():
    song_id = input('please input the id of the song you want to download:')
    song_name = input('please input the name of the song you want to download:')
    print('song downloading,please wait for a while...')
    GetMusic(song_id,song_name)
    return None

main()
