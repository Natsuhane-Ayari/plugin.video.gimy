import os
import sys
import requests
import bs4
import opencc

user_agent = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71'}

def getHomePage():
    href = []
    res = requests.get("https://gimy.app/",headers=user_agent).text
    soup = bs4.BeautifulSoup(res,'html.parser')
    homePage = soup.find_all("a",class_="video-pic loading")
    for i in range(len(homePage)):
        #listitem = xbmcgui.ListItem("%s"%(homePage[i].get("title")))
        #listitem.setArt({'thumb':'%s'%(homePage[i].get("data-original"))})
        #xbmcplugin.addDirectoryItem(handle,sys.argv[0]+"?lines1H%dH%d"%(i,handle),listitem,True)
        #href.append("https://gimy.app%s"%(homePage[i].get("href")))
        print(homePage[i].get("href").split("/")[-1][:-5])

def getanime():
    #album_code = xbmcgui.Dialog().input("輸入影集號碼")
    res = requests.get("https://gimy.app/vod/%s.html"%("227096")).text
    soup = bs4.BeautifulSoup(res)
    album_title = soup.find("meta",property="og:image").get("content")
    print(album_title)
    #print(album_title)

def getTypeAnime():
    href = []
    res = requests.get("https://gimy.app/type/30.html").text
    soup = bs4.BeautifulSoup(res)
    anime = soup.find_all("a",class_="video-pic loading")
    for i in range(len(anime)):
        listitem = xbmcgui.ListItem("%s"%(anime[i].get("title")))
        listitem.setArt({'thumb':'%s'%(anime[i].get("data-original"))})
        xbmcplugin.addDirectoryItem(handle,sys.argv[0]+"?linesH%d"%(i),listitem,True)
        href.append("https://gimy.app%s"%(anime[i].get("href")))
    return href

def opencctest():
    text = "为什么"
    text = opencc.OpenCC("s2tw").convert(text)
    print(text)

def search():
    res = requests.get("https://gimy.app/search/-------------.html?wd=間諜家家酒").text
    print(res)

def search(key_word):
    href = []
    res = requests.get("https://gimy.app/search/-------------.html?wd=%s"%(key_word)).text
    soup = bs4.BeautifulSoup(res)
    search = soup.find_all("a",class_="video-pic loading")
    for i in range(len(search)):
        listitem = xbmcgui.ListItem("%s"%(search[i].get("title")))
        listitem.setArt({'thumb':'%s'%(search[i].get("data-original"))})
        xbmcplugin.addDirectoryItem(handle,sys.argv[0]+"?lines1H%d"%(i),listitem,True)
        href.append("https://gimy.app%s"%(search[i].get("href")))

def search2(index):
    href = []
    res = requests.get("https://gimy.app/type/30.html").text
    soup = bs4.BeautifulSoup(res)
    search = soup.find_all("a",class_="video-pic loading")
    for i in range(len(search)):
        href.append("https://gimy.app%s"%(search[i].get("href")))
    get_playlist(href[index])

getHomePage()