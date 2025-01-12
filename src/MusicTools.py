import requests
import re
class MusicTools:
    def __init__(self):
        self.songsList = []
    def getMusicListByNameId(self, id):
        url = 'http://localhost:3000/artist/songs?id=' + id
        r = requests.get(url)
        self.songsList = r.json()['songs']
    def downloadMusic(self):
        global songsName
        musicIds = []
        for song in self.songsList:
            musicIds.append(str(song['id']))
        ids = ",".join(musicIds)
        print(",".join(musicIds))
        url = 'http://localhost:3000/song/url/v1?id=' + ids +'&level=lossless'
        res = requests.get(url)
        dataList = res.json()['data']
        tempList = []
        # 过滤掉小于2M的数据
        for data in dataList:
            if data['size'] / 1024 / 1024 >= 2:
                tempList.append(data)
        for index,data in enumerate(tempList):
            songsName = self.songsList[index]['name']
            try:
                print("共%d首，正在下载：%s,当前第%d首" % (len(tempList), songsName, index+1))
                res = requests.get(data['url'])
                self.getLyricsBySongsId(str(data['id']),songsName)
                # 写入文件保存
                with open ('../music/%s.mp3' % songsName, 'wb') as f:
                    f.write(res.content)
                    f.close()
            except Exception as e:
                print(e)
        print("下载完成")
    def getLyricsBySongsId(self, id,name):
        url = 'http://localhost:3000/lyric?id='+ id
        res = requests.get(url).json()
        with open('../lyric/%s.lrc' % name, 'w',encoding='utf-8') as f:
            f.write(res['lrc']['lyric'])
            f.close()
if __name__ == '__main__':
    music = MusicTools()
    songsId = str(input('请输入歌手id:'))
    music.getMusicListByNameId(songsId)
    music.downloadMusic()
