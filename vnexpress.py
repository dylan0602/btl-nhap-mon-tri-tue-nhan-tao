from bs4 import BeautifulSoup
import requests

def getNews():
    list_news = []
    r = requests.get("https://vnexpress.net/")
    soup = BeautifulSoup(r.text, 'html.parser')
    mydivs = soup.find_all("h3", {"class": "title-news"})

    for new in mydivs:
        newsdict = {}
        newsdict["link"] = new.a.get("href")
        newsdict["title"] = new.a.get("title")
        list_news.append(newsdict)

    return list_news

