import requests
from bs4 import BeautifulSoup

def get_trending():
    response = requests.get('https://mydramalist.com/shows/top_airing')
    soup = BeautifulSoup(response.content, 'html.parser')
    trending = {}
    titles = []
    info = []

    results = soup.find('div', class_="m-t nav-active-border b-primary").find_all('div', class_='box')
    for item in results:
        titles.append('**'+(item.find('h6').find('a').text)+'**')
        info.append(item.find('span', class_='text-muted').text)
    
    i=1
    while i<11:
        trending[i] = titles[i-1]+" ("+info[i-1]+")"
        i+=1
    return trending