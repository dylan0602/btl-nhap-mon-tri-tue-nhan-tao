from bs4 import BeautifulSoup
import requests


def getNews():
    list_news=[]
    r = requests.get('https://cryptonews.net/')
    soup = BeautifulSoup(r.text, 'html.parser')
    for item in soup.find_all('a',class_='title'):
        newsdict={}
        newsdict["link"]=f'https://cryptonews.net{item["href"]}'
        newsdict["title"]=item.text
        list_news.append(newsdict)

    return list_news
