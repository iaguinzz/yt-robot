import sys

from data import *
from googleapiclient.discovery import build
import youtube_dl

class Yt:
    def __init__(self):
        self.endpoint = 'https://www.youtube.com/watch?v='

        self.yt = build('youtube', 'v3', developerKey=api_key)

    def getLinkOne(self, musicName, f='mp3', file=False):
        if file:
            filee = open(musicName,)
            linhas = filee.readlines()
            for linha in linhas:
                req = self.yt.search().list(q=linha, part='snippet', type='video')
                res = req.execute()
                titleMusic = res['items'][0]['snippet']['title']
                idMusic = res['items'][0]['id']['videoId']
                print('nome da música: {}\nid da música: {}'.format(titleMusic, idMusic))
                self.downloadMusic(idMusic, f)

    def downloadMusic(self, ide, formato):
        url = self.endpoint+ide
        ydlOpt = {'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': formato,
        'preferredquality': '192',
    }],}
        ydl = youtube_dl.YoutubeDL(ydlOpt)
        ydl.download([url])

lArgv = len(sys.argv)
if lArgv >= 2:
    yt = Yt()
    if 'video' in sys.argv[1]:
        yt.getLinkOne(sys.argv[2], f='mp4')

    elif 'arquivo' in sys.argv[1]:
        print(sys.argv)
        yt.getLinkOne(sys.argv[2], file=True)

    else:
        yt.getLinkOne(sys.argv[1])

else:
    print('Uso: python main.py [OPÇÃO] [ARQUIVO OU NOME DA MUSICA]')
    print('Exemplo : python main.py --arquivo listademusicas.txt')
    print('Exemplo : python main.py "Racionais MCS negro drama"')