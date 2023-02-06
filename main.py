import xbmcplugin, xbmcgui, xbmc, xbmcvfs
import sys
import requests
import bs4
import opencc
import json

temp_PATH = xbmcvfs.translatePath("special://home/").replace("\\","/")+"addons/plugin.video.gimy/temp/"
user_agent = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71'}

def getHomePage():
    res = requests.get("https://gimy.app/",headers=user_agent).text
    soup = bs4.BeautifulSoup(res,'html.parser')
    homePage = soup.find_all("a",class_="video-pic loading")
    for i in range(len(homePage)):
        listitem = xbmcgui.ListItem("%s"%(homePage[i].get("title")))
        listitem.setArt({'thumb':'%s'%(homePage[i].get("data-original"))})
        xbmcplugin.addDirectoryItem(handle,sys.argv[0]+"?coderesH%s"%(homePage[i].get("href").split("/")[-1][:-5]),listitem,True)

def getTypeAnime():
    res = requests.get("https://gimy.app/type/30.html",headers=user_agent).text
    soup = bs4.BeautifulSoup(res,'html.parser')
    anime = soup.find_all("a",class_="video-pic loading")
    for i in range(len(anime)):
        listitem = xbmcgui.ListItem("%s"%(anime[i].get("title")))
        listitem.setArt({'thumb':'%s'%(anime[i].get("data-original"))})
        xbmcplugin.addDirectoryItem(handle,sys.argv[0]+"?coderesH%s"%(anime[i].get("href").split("/")[-1][:-5]),listitem,True)

def getTypeTVShow():
    res = requests.get("https://gimy.app/type/2.html",headers=user_agent).text
    soup = bs4.BeautifulSoup(res,'html.parser')
    tvshow = soup.find_all("a",class_="video-pic loading")
    for i in range(len(tvshow)):
        listitem = xbmcgui.ListItem("%s"%(tvshow[i].get("title")))
        listitem.setArt({'thumb':'%s'%(tvshow[i].get("data-original"))})
        xbmcplugin.addDirectoryItem(handle,sys.argv[0]+"?coderesH%s"%(tvshow[i].get("href").split("/")[-1][:-5]),listitem,True)

def getTypeVarietyShow():
    res = requests.get("https://gimy.app/type/29.html",headers=user_agent).text
    soup = bs4.BeautifulSoup(res,'html.parser')
    varietyshow = soup.find_all("a",class_="video-pic loading")
    for i in range(len(varietyshow)):
        listitem = xbmcgui.ListItem("%s"%(varietyshow[i].get("title")))
        listitem.setArt({'thumb':'%s'%(varietyshow[i].get("data-original"))})
        xbmcplugin.addDirectoryItem(handle,sys.argv[0]+"?coderesH%s"%(varietyshow[i].get("href").split("/")[-1][:-5]),listitem,True)

def search(key_word):
    res = requests.get("https://gimy.app/search/-------------.html?wd=%s"%(key_word),headers=user_agent).text
    soup = bs4.BeautifulSoup(res,'html.parser')
    search = soup.find_all("a",class_="video-pic loading")
    for i in range(len(search)):
        listitem = xbmcgui.ListItem("%s"%(search[i].get("title")))
        listitem.setArt({'thumb':'%s'%(search[i].get("data-original"))})
        xbmcplugin.addDirectoryItem(handle,sys.argv[0]+"?coderesH%s"%(search[i].get("href").split("/")[-1][:-5]),listitem,True)

def find_m3u8(urlData): #取得單一集數m3u8
    res = requests.get(urlData,headers=user_agent)
    soup = bs4.BeautifulSoup(res.text,'html.parser')
    urlData = soup.find(id='zanpiancms_player').find_next('script').text.split('"')[25]
    URL = ""
    for i in range(len(urlData)):
        if(urlData[i] == "\\"):
            continue
        else:
            URL = URL+urlData[i]
    print(URL)
    return URL

def cut_node(data):
    loca = 0
    for i in range(len(data)):
        if data[i] == "/":
            loca = i
    parent_node = data[:loca:]
    return parent_node

def write_in_multipleFiles(playList,start,end):
    f = open(temp_PATH+"rmad.txt")
    yun = json.loads(f.readlines()[0])
    f.close()
    if yun[-1] == "true":
        #跳廣告
        m3u8_url = find_m3u8(playList[start])
        res = requests.get(m3u8_url,headers=user_agent).text
        parent_node = cut_node(m3u8_url)
        m3u8_url = "%s/%s"%(parent_node,res.split('\n')[2])
        res = requests.get(m3u8_url,headers=user_agent).text
        ad_status = 0
        ready_write = ""
        f = open(temp_PATH+"%d.m3u8"%(start+1),"w")
        for j in res:
            if j == "\n":
                if ready_write == "#EXT-X-DISCONTINUITY":
                    if ad_status == 0:
                        ad_status = 1
                    elif ad_status == 1:
                        ad_status = 0
                        ready_write = "#removed ads"
                if ad_status == 0:
                    if ready_write[0] != "#":
                        f.write("%s/%s\n"%(cut_node(m3u8_url),ready_write))
                    else:
                        f.write("%s\n"%(ready_write))
                    ready_write = ""
                else:
                    ready_write = ""
            else:
                ready_write+=j
        f.close()
        listitem = xbmcgui.ListItem("第%d集"%(start+1))
        xbmc.Player().play(temp_PATH+"%d.m3u8"%(start+1), listitem)
    else:
        m3u8_url = find_m3u8(playList[start])
        #xbmcgui.Dialog().ok("test","%s"%(m3u8_url))
        listitem = xbmcgui.ListItem("第%d集"%(start+1))
        xbmc.Player().play(m3u8_url, listitem)

write_mode = "w"
start = 1
end = 0
output_mode = 1 #1代表去掉廣告分割檔案，2代表維持單一檔案
album_title = "NULL"
playitem = []
#href = []

def get_playlist(album):
    global end
    global album_title
    #album = sys.argv[-1]
    res = requests.get(album,headers=user_agent)
    soup = bs4.BeautifulSoup(res.text,'html.parser')
    album_title = soup.find('h1').text[:-2:]
    rmad = []
    print(album_title)
    lines = soup.find_all(class_='gico')
    for i in range(len(lines)):
        #print("[%3d] %s"%(i,lines[i].text))
        listitem = xbmcgui.ListItem("[%3d] %s"%(i,lines[i].text))
        xbmcplugin.addDirectoryItem(handle,sys.argv[0]+"?epH%d"%(i),listitem,True)
        if "順暢雲" in lines[i].text or "飛翔雲" in lines[i].text:
            rmad.append("%d"%(i))
    rmad.append("unknow")
    f = open(temp_PATH+"rmad.txt","w")
    f.write(json.dumps(rmad))
    f.close()
    f = open(temp_PATH+"album.txt","w")
    f.write(album)
    f.close()

def select_EP(index):
    lines_Select = index
    f = open(temp_PATH+"album.txt","r")
    album = ""
    for i in f:
        if i != '\n':
            album+=i
        else:
            break
    f.close()
    
    res = requests.get(album,headers=user_agent)
    soup = bs4.BeautifulSoup(res.text,'html.parser')
    #print("="*50)
    #for i in lines:
    #    print(i)
    #print("="*50)
    playListSource = soup.find_all(class_='clearfix fade in active')
    #EP = playListSource.find_next('li')
    #print(playListSource[lines_Select])
    soup = bs4.BeautifulSoup(str(playListSource[lines_Select]),'html.parser')
    playListSource = soup.find_all('a')
    #print(playListSource)
    f = open(temp_PATH+"playList.txt","w")
    playList = [] #單一集數的原始網址
    for i in range(len(playListSource)):
        playList.append("https://gimy.app/"+str(playListSource[i]).split('"')[1])
        listitem = xbmcgui.ListItem("第%d集"%(i+1))
        f.write("https://gimy.app/"+str(playListSource[i]).split('"')[1]+"\n")
        xbmcplugin.addDirectoryItem(handle,sys.argv[0]+"?playH%d"%(i),listitem,False)
    f.close()
    f = open(temp_PATH+"rmad.txt","r")
    yun = json.loads(f.readlines()[0])
    f.close()
    if str(index) in yun:
        yun[-1] = "true"
    else:
        yun[-1] = "false"
    f = open(temp_PATH+"rmad.txt","w")
    f.write(json.dumps(yun))
    f.close()
    #if end == 0:
        #end = len(playList)
    #print(playList)
    #write_in_multipleFiles(playList,0,len(playList))
    #return playList


least = 0
handle=int(sys.argv[1])
dir_level=0
isFolder=True

dir_level=sys.argv[2][1:].split('H')
url="www"#sys.argv[0]+'?'+str(dir_level+1)
if dir_level==4:
    isFolder=False
    url='http://tv1.btv.com.cn/asset/2012/03/27/BTV1_20120327_183405049_742928_23560.mp4'

'''for i in range(dirs[dir_level][1]):
    listitem=xbmcgui.ListItem(name1[i]+str(i+1))
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)'''
#1:首頁 2:動漫
if dir_level[0] == "":
    listitem = xbmcgui.ListItem("首頁")
    xbmcplugin.addDirectoryItem(handle,sys.argv[0]+'?1',listitem,True)
    listitem = xbmcgui.ListItem("動漫")
    xbmcplugin.addDirectoryItem(handle,sys.argv[0]+'?2',listitem,True)
    listitem = xbmcgui.ListItem("電視劇")
    xbmcplugin.addDirectoryItem(handle,sys.argv[0]+'?3',listitem,True)
    listitem = xbmcgui.ListItem("綜藝")
    xbmcplugin.addDirectoryItem(handle,sys.argv[0]+'?4',listitem,True)
    listitem = xbmcgui.ListItem("輸入影集號碼")
    xbmcplugin.addDirectoryItem(handle,sys.argv[0]+'?7',listitem,True)
    listitem = xbmcgui.ListItem("搜尋")
    xbmcplugin.addDirectoryItem(handle,sys.argv[0]+'?8',listitem,True)
if dir_level[0] == "1":
    getHomePage()
if dir_level[0] == "2":
    getTypeAnime()
if dir_level[0] == "3":
    getTypeTVShow()
if dir_level[0] == "4":
    getTypeVarietyShow()
if dir_level[0] == "7":
    album_code = xbmcgui.Dialog().input("輸入影集號碼")
    res = requests.get("https://gimy.app/vod/%s.html"%(album_code),headers=user_agent).text
    soup = bs4.BeautifulSoup(res,'html.parser')
    album_title = soup.find("h1").text
    album_thumb = soup.find("meta",property="og:image").get("content")
    listitem = xbmcgui.ListItem(album_title)
    listitem.setArt({'thumb':album_thumb})
    xbmcplugin.addDirectoryItem(handle,sys.argv[0]+'?coderesH'+album_code,listitem,True)
if dir_level[0] == "8":
    key_word = xbmcgui.Dialog().input("搜尋")
    key_word = opencc.OpenCC("s2tw").convert(key_word)
    f = open(temp_PATH+"encode.txt","w")
    for i in key_word:
        f.write(str(ord(i))+"\n")
    f.close()
    search(key_word)
if dir_level[0] == "coderes":
    get_playlist("https://gimy.app/vod/%s.html"%(dir_level[1]))
if dir_level[0] == "ep":
    select_EP(int(dir_level[1]))
if dir_level[0] == "play":
    ep = int(dir_level[1])
    f = open(temp_PATH+"playList.txt","r")
    for i in f.readlines():
        playitem.append(i.strip())
    f.close()
    write_in_multipleFiles(playitem,ep,ep)

#xbmcgui.Dialog().ok("info","%s\n%s\n%s"%(sys.argv[0],sys.argv[2],sys.argv[1]))
xbmcplugin.endOfDirectory(handle)
