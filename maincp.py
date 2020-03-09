import os
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from data import *
from googleapiclient.discovery import build
import youtube_dl

class Yt:
    def __init__(self):
        self.endpoint = 'https://www.youtube.com/watch?v='
        self.opt = webdriver.ChromeOptions()
        self.opt.add_argument('headless')
        #self.opt.add_experimental_option("mobileEmulation", {"deviceName" : "Nexus 5"})
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.opt)

        self.vaga = 'https://www.vagalume.com.br/top100/artistas/nacional/2020/02/'
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
        file = open('ondeparei.txt')
        lineOfFile = file.readlines()
        artistLink = lineOfFile[0]
        artistLink = artistLink.replace('\n','')
        file.close()
        try:
            self.driver.get(self.vaga)
            artistasEL = self.driver.find_elements_by_class_name('h22')
            listaDeArtistasLink = []
        except Exception as e:
            print(e)
            print('erro ao pegar o link dos artistas')
        try:
            c = 0
            for i in artistasEL:
                if c ==0:
                    c+=1
                    pass
                else:
                    a = i.get_attribute('href')
                    listaDeArtistasLink.append(a)
            print(listaDeArtistasLink)

        except Exception as e:
            print(e)
            print('erro ao colocar os links dos artistas na lista')

        try:
            print(artistLink)
            indexN = listaDeArtistasLink.index(artistLink)
            print(indexN)
            print(len(listaDeArtistasLink))
            for m in range(0,indexN):
                listaDeArtistasLink.pop(0)
        except Exception as e:
            print('erro no file: '.format(e))
        try:
            for i in listaDeArtistasLink:
                arq = open('ondeparei.txt', 'w')
                arq.write(i)
                arq.close()
                listaDeMusicas = []
                self.driver.get(i)
                musicNameEl = self.driver.find_elements_by_class_name('nameMusic')
                for j in musicNameEl:
                    musicNameText = j.get_attribute('innerText')
                    listaDeMusicas.append(musicNameText)
                for l in listaDeMusicas:
                        print('lista de música: {}'.format(listaDeMusicas))
                        print('lista de Artistas: {}'.format(listaDeArtistasLink))
                        #print(l)
                        genList = []
                        gens = ''
                        try:
                            try:
                                for p in range(1,7):
                                    genEl = self.driver.find_element_by_xpath('//*[@id="artHeaderTitle"]/div/ul/li[{}]'.format(p))
                                    genText = genEl.get_attribute('innerText')
                                    genList.append(genText)
                            except Exception as e:
                                print('erro ao pegar os generos')
                                print(e)
                            lendeGenlist = len(genList)
                            for gen in range(0,lendeGenlist):
                                gens += genList[gen]
                                if gen == lendeGenlist-1:
                                    pass
                                else:
                                    gens += ' e '
                            nameOfTheBand = self.driver.find_element_by_xpath('//*[@id="artHeaderTitle"]/h1/a').get_attribute('innerText')
                            nameOfTheBand = nameOfTheBand.replace("'",'')
                            nameOfTheBand = nameOfTheBand.replace('"','')
                            gens = "'{}'".format(gens)
                            art = "'{}'".format(nameOfTheBand)
                            dir1 = 'mkdir {}/{}'.format(os.getcwd(), gens)
                            dir2 = 'mkdir {}/{}/{}'.format(os.getcwd(),gens, art)
                            path = '{}/{}'.format(gens, art)
                            cmds = [dir1,dir2]

                            for cmd in cmds:
                                print(cmd)
                                os.system(cmd)

                        except Exception as e:
                            print('erro ao criar dirétorio')
                            print(e)


                        self.getLinkOne(l,path=path)
                        os.system('mv *.mp3 {}'.format(path))
        except Exception as e:
            print(e)
            print('erro no maior for')


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