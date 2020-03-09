import os
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from data import *
from googleapiclient.discovery import build
import youtube_dl
import time

class Yt:
    def __init__(self):
        self.endpoint = 'https://www.youtube.com/watch?v='
        self.opt = webdriver.ChromeOptions()
        #self.opt.add_argument('headless')
        #self.opt.add_experimental_option("mobileEmulation", {"deviceName" : "Nexus 5"})
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.opt)

        self.vagaURL = 'https://www.vagalume.com.br/browse/style/'
        self.yt = build('youtube', 'v3', developerKey=api_key)

    def getLinkOne(self, musicName, f='mp3', file=False, path=''):
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
        else:
            req = self.yt.search().list(q=musicName, part='snippet', type='video')
            res = req.execute()
            titleMusic = res['items'][0]['snippet']['title']
            idMusic = res['items'][0]['id']['videoId']
            print('nome da música: {}\nid da música: {}'.format(titleMusic, idMusic))
            self.downloadMusic(idMusic, f)

    def downloadMusic(self, ide, formato,path=''):
        url = self.endpoint+ide
        ydlOpt = {
        'outtmpl' : '%(title)s.%(ext)s',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': formato,
        'preferredquality': '192',
    }],}
        ydl = youtube_dl.YoutubeDL(ydlOpt)
        ydl.download([url])


    def Vagalume(self):
        self.driver.get(self.vagaURL)
        self.driver.find_element_by_xpath('//*[@id="body"]/div[3]/div[1]/ul/li[1]').click()
        time.sleep(6)
        j=1
        linkArtistaList = []
        nameArtista = []
        while True:
            try:
                liArtista = self.driver.find_element_by_xpath(f'//*[@id="pushStateView"]/div[2]/ul[3]/li[{j}]')
                j+=1
            except:
                j=1
                break
            
            aArtista = liArtista.find_element_by_tag_name('a')
            linkArtista = aArtista.get_attribute('href')
            linkArtistaList.append(linkArtista)
            
            pArtista = liArtista.find_element_by_tag_name('p')
            textArtista = pArtista.get_attribute('innerText')
            nameArtista.append(textArtista)
        print(f'Nome dos Artistas: {nameArtista}')
        print(f'Link dos Artistas: {linkArtistaList}')

        for o in range(0, len(linkArtistaList)):
            self.driver.get(linkArtistaList[o])
            time.sleep(6)
            
            print(f'Nome do Artista: {nameArtista[o]}')
            i = 1
            while True:
                try:
                    liMusica = self.driver.find_element_by_xpath(f'//*[@id="alfabetMusicList"]/li[{i}]')
                    if i == 100 or i == 200 or i == 300:
                        self.driver.execute_script("return arguments[0].scrollIntoView();", liMusica)
                    i+=1
                except Exception as e:
                    j=1
                    print('loop breaked')
                    break
                try:
                    a = liMusica.find_element_by_tag_name('a')
                    textNameMusic = a.get_attribute('innerText') ######## nome da música
                    print(f'Música: {textNameMusic}')
                except:
                    pass
                
                
                
        time.sleep(10)

    def __del__(self):
        self.driver.close()

yt = Yt()
yt.Vagalume()

















# lArgv = len(sys.argv)
# if lArgv >= 2:
#     yt = Yt()
#     if 'video' in sys.argv[1]:
#         yt.getLinkOne(sys.argv[2], f='mp4')
#
#     elif 'arquivo' in sys.argv[1]:
#         print(sys.argv)
#         yt.getLinkOne(sys.argv[2], file=True)
#
#     else:
#         yt.getLinkOne(sys.argv[1])
#
# else:
#     print('Uso: python main.py [OPÇÃO] [ARQUIVO OU NOME DA MUSICA]')
#     print('Exemplo : python main.py --arquivo listademusicas.txt')
#     print('Exemplo : python main.py "Racionais MCS negro drama"')