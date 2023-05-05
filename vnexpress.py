import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
path = ""
def getNews():
    list_news = []
    r = requests.get(f"https://vnexpress.net/{path}")
    soup = BeautifulSoup(r.text, 'html.parser')
    mydivs = soup.find_all("h3", {"class": "title-news"})

    for new in mydivs:
        newsdict = {}
        newsdict["link"] = new.a.get("href")
        newsdict["title"] = new.a.get("title")
        list_news.append(newsdict)

    return list_news
def getContents(url):
    s = requests.get(url)
    soup = BeautifulSoup(s.content, "html.parser")
    article = soup.find_all('div',class_='desc_cation',style=None) or soup.find_all('p',class_='Normal')
    res = ""
    line = ['']
    element = soup.find('h1', class_='title-detail')
    res += element.text+'\n'
    for a in article:
        line.append(a.text)
    for i in line:
        res+=i+'\n'
    return res


def set_path(p):
    global path
    path = unidecode(p).lower()
def get_path():
    return path

